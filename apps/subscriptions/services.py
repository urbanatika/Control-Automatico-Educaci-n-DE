from datetime import datetime, timezone as dt_timezone

import stripe
from django.conf import settings

from .models import Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY

PLAN_BY_PRICE_ID = {
    settings.STRIPE_MONTHLY_PRICE_ID: Subscription.Plan.MONTHLY,
    settings.STRIPE_ANNUAL_PRICE_ID: Subscription.Plan.ANNUAL,
}


def get_or_create_local_subscription(user) -> Subscription:
    subscription, _ = Subscription.objects.get_or_create(user=user)
    return subscription


def get_or_create_stripe_customer(user) -> str:
    subscription = get_or_create_local_subscription(user)
    if subscription.stripe_customer_id:
        return subscription.stripe_customer_id

    customer = stripe.Customer.create(email=user.email, name=user.get_full_name() or user.username)
    subscription.stripe_customer_id = customer["id"]
    subscription.save(update_fields=["stripe_customer_id"])
    return customer["id"]


def create_checkout_session(user, price_id: str, success_url: str, cancel_url: str):
    customer_id = get_or_create_stripe_customer(user)
    return stripe.checkout.Session.create(
        customer=customer_id,
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=success_url,
        cancel_url=cancel_url,
        client_reference_id=str(user.id),
    )


def create_billing_portal_session(user, return_url: str):
    customer_id = get_or_create_stripe_customer(user)
    return stripe.billing_portal.Session.create(customer=customer_id, return_url=return_url)


def _sync_from_stripe_subscription(stripe_subscription: dict) -> None:
    customer_id = stripe_subscription["customer"]
    try:
        subscription = Subscription.objects.get(stripe_customer_id=customer_id)
    except Subscription.DoesNotExist:
        return

    subscription.stripe_subscription_id = stripe_subscription["id"]
    subscription.status = stripe_subscription["status"]

    price_id = stripe_subscription["items"]["data"][0]["price"]["id"]
    subscription.plan = PLAN_BY_PRICE_ID.get(price_id, subscription.plan)

    period_end = stripe_subscription.get("current_period_end")
    if period_end:
        subscription.current_period_end = datetime.fromtimestamp(period_end, tz=dt_timezone.utc)

    subscription.save()


def handle_webhook_event(event: dict) -> None:
    event_type = event["type"]
    data_object = event["data"]["object"]

    if event_type == "checkout.session.completed":
        stripe_subscription = stripe.Subscription.retrieve(data_object["subscription"])
        _sync_from_stripe_subscription(stripe_subscription)
    elif event_type in ("customer.subscription.updated", "customer.subscription.created"):
        _sync_from_stripe_subscription(data_object)
    elif event_type == "customer.subscription.deleted":
        try:
            subscription = Subscription.objects.get(stripe_customer_id=data_object["customer"])
        except Subscription.DoesNotExist:
            return
        subscription.status = Subscription.Status.CANCELED
        subscription.save(update_fields=["status", "updated_at"])
