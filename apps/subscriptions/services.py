import hashlib
import hmac

import requests
from django.conf import settings
from django.utils.dateparse import parse_datetime

from .models import Subscription

API_BASE = "https://api.mercadopago.com"


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {settings.MERCADOPAGO_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }


def _plan_amount(plan: str) -> int:
    return (
        settings.MERCADOPAGO_ANNUAL_AMOUNT_CLP
        if plan == Subscription.Plan.ANNUAL
        else settings.MERCADOPAGO_MONTHLY_AMOUNT_CLP
    )


def _plan_frequency_months(plan: str) -> int:
    return 12 if plan == Subscription.Plan.ANNUAL else 1


def get_or_create_local_subscription(user) -> Subscription:
    subscription, _ = Subscription.objects.get_or_create(user=user)
    return subscription


def create_preapproval(user, plan: str, back_url: str) -> dict:
    plan_label = dict(Subscription.Plan.choices).get(plan, plan)
    payload = {
        "reason": f"Suscripción {plan_label} — {settings.SITE_NAME}",
        "external_reference": str(user.id),
        "payer_email": user.email,
        "back_url": back_url,
        "auto_recurring": {
            "frequency": _plan_frequency_months(plan),
            "frequency_type": "months",
            "transaction_amount": _plan_amount(plan),
            "currency_id": "CLP",
        },
    }
    response = requests.post(f"{API_BASE}/preapproval", json=payload, headers=_headers(), timeout=15)
    response.raise_for_status()
    data = response.json()

    subscription = get_or_create_local_subscription(user)
    subscription.plan = plan
    subscription.mercadopago_preapproval_id = data["id"]
    subscription.mercadopago_payer_email = user.email
    subscription.status = data.get("status", Subscription.Status.PENDING)
    subscription.save()

    return data


def fetch_preapproval(preapproval_id: str) -> dict:
    response = requests.get(f"{API_BASE}/preapproval/{preapproval_id}", headers=_headers(), timeout=15)
    response.raise_for_status()
    return response.json()


def cancel_preapproval(subscription: Subscription) -> None:
    if not subscription.mercadopago_preapproval_id:
        subscription.status = Subscription.Status.CANCELLED
        subscription.save(update_fields=["status", "updated_at"])
        return

    response = requests.put(
        f"{API_BASE}/preapproval/{subscription.mercadopago_preapproval_id}",
        json={"status": "cancelled"},
        headers=_headers(),
        timeout=15,
    )
    response.raise_for_status()
    subscription.status = Subscription.Status.CANCELLED
    subscription.save(update_fields=["status", "updated_at"])


def sync_from_preapproval_data(data: dict) -> None:
    preapproval_id = data.get("id")
    if not preapproval_id:
        return

    try:
        subscription = Subscription.objects.get(mercadopago_preapproval_id=preapproval_id)
    except Subscription.DoesNotExist:
        external_reference = data.get("external_reference")
        if not external_reference:
            return
        from apps.accounts.models import User

        try:
            user = User.objects.get(pk=external_reference)
        except (User.DoesNotExist, ValueError):
            return
        subscription = get_or_create_local_subscription(user)
        subscription.mercadopago_preapproval_id = preapproval_id

    status = data.get("status")
    if status in Subscription.Status.values:
        subscription.status = status

    subscription.mercadopago_payer_email = data.get("payer_email") or subscription.mercadopago_payer_email

    next_payment_date = data.get("next_payment_date")
    if next_payment_date:
        subscription.next_payment_date = parse_datetime(next_payment_date)

    subscription.save()


def verify_webhook_signature(x_signature: str, x_request_id: str, data_id: str) -> bool:
    """https://www.mercadopago.com/developers/en/docs/checkout-api/webhooks/checking-signature"""
    if not settings.MERCADOPAGO_WEBHOOK_SECRET:
        return True

    parts = dict(part.split("=", 1) for part in x_signature.split(",") if "=" in part)
    ts = parts.get("ts")
    v1 = parts.get("v1")
    if not ts or not v1:
        return False

    manifest = f"id:{data_id.lower()};request-id:{x_request_id};ts:{ts};"
    expected = hmac.new(
        settings.MERCADOPAGO_WEBHOOK_SECRET.encode(), manifest.encode(), hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, v1)
