import json

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View

from . import services


class PricingView(TemplateView):
    template_name = "subscriptions/pricing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mercadopago_configured"] = bool(
            settings.MERCADOPAGO_ACCESS_TOKEN and settings.MERCADOPAGO_MONTHLY_AMOUNT_CLP
        )
        context["monthly_price_clp"] = f"{settings.MERCADOPAGO_MONTHLY_AMOUNT_CLP:,}".replace(",", ".")
        context["annual_price_clp"] = f"{settings.MERCADOPAGO_ANNUAL_AMOUNT_CLP:,}".replace(",", ".")
        if self.request.user.is_authenticated:
            context["subscription"] = getattr(self.request.user, "subscription", None)
        return context


class CreateCheckoutSessionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        plan = request.POST.get("plan", "monthly")

        if not settings.MERCADOPAGO_ACCESS_TOKEN:
            messages.error(
                request,
                "El pago aún no está configurado. Agrega tu Access Token de Mercado Pago en el archivo .env.",
            )
            return redirect("subscriptions:pricing")

        back_url = request.build_absolute_uri(reverse("subscriptions:success"))

        try:
            preapproval = services.create_preapproval(request.user, plan, back_url)
        except requests.RequestException as exc:
            messages.error(request, f"No se pudo iniciar el pago con Mercado Pago: {exc}")
            return redirect("subscriptions:pricing")

        return redirect(preapproval["init_point"], permanent=False)


class UnsubscribeConfirmView(LoginRequiredMixin, TemplateView):
    template_name = "subscriptions/unsubscribe_confirm.html"


class UnsubscribeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        subscription = getattr(request.user, "subscription", None)
        if subscription:
            try:
                services.cancel_preapproval(subscription)
                messages.success(request, "Tu suscripción fue cancelada.")
            except requests.RequestException as exc:
                messages.error(request, f"No se pudo cancelar la suscripción: {exc}")
        return redirect("accounts:dashboard")


class SuccessView(LoginRequiredMixin, TemplateView):
    template_name = "subscriptions/success.html"


@method_decorator(csrf_exempt, name="dispatch")
class MercadoPagoWebhookView(View):
    def post(self, request, *args, **kwargs):
        topic = request.GET.get("type") or request.GET.get("topic")
        data_id = request.GET.get("data.id") or request.GET.get("id")

        if not data_id and request.body:
            try:
                payload = json.loads(request.body)
            except ValueError:
                payload = {}
            data_id = payload.get("data", {}).get("id")
            topic = topic or payload.get("type")

        if not data_id or topic not in ("preapproval", "subscription_preapproval"):
            return HttpResponse(status=200)

        x_signature = request.META.get("HTTP_X_SIGNATURE", "")
        x_request_id = request.META.get("HTTP_X_REQUEST_ID", "")
        if x_signature and not services.verify_webhook_signature(x_signature, x_request_id, str(data_id)):
            return HttpResponseBadRequest("Firma inválida")

        try:
            preapproval_data = services.fetch_preapproval(data_id)
        except requests.RequestException:
            return HttpResponse(status=200)

        services.sync_from_preapproval_data(preapproval_data)
        return HttpResponse(status=200)
