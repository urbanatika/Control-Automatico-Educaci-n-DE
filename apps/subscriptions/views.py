import stripe
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
        context["stripe_configured"] = bool(settings.STRIPE_SECRET_KEY and settings.STRIPE_MONTHLY_PRICE_ID)
        if self.request.user.is_authenticated:
            context["subscription"] = getattr(self.request.user, "subscription", None)
        return context


class CreateCheckoutSessionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        plan = request.POST.get("plan", "monthly")
        price_id = (
            settings.STRIPE_ANNUAL_PRICE_ID if plan == "annual" else settings.STRIPE_MONTHLY_PRICE_ID
        )

        if not settings.STRIPE_SECRET_KEY or not price_id:
            messages.error(
                request,
                "El pago aún no está configurado. Agrega tus claves de Stripe en el archivo .env.",
            )
            return redirect("subscriptions:pricing")

        success_url = request.build_absolute_uri(reverse("subscriptions:success"))
        cancel_url = request.build_absolute_uri(reverse("subscriptions:cancel"))

        try:
            session = services.create_checkout_session(request.user, price_id, success_url, cancel_url)
        except stripe.error.StripeError as exc:
            messages.error(request, f"No se pudo iniciar el pago: {exc.user_message or exc}")
            return redirect("subscriptions:pricing")

        return redirect(session.url, permanent=False)


class BillingPortalView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not settings.STRIPE_SECRET_KEY:
            messages.error(request, "El pago aún no está configurado.")
            return redirect("accounts:dashboard")

        return_url = request.build_absolute_uri(reverse("accounts:dashboard"))
        try:
            session = services.create_billing_portal_session(request.user, return_url)
        except stripe.error.StripeError as exc:
            messages.error(request, f"No se pudo abrir el portal de facturación: {exc.user_message or exc}")
            return redirect("accounts:dashboard")

        return redirect(session.url, permanent=False)


class SuccessView(LoginRequiredMixin, TemplateView):
    template_name = "subscriptions/success.html"


class CancelView(TemplateView):
    template_name = "subscriptions/cancel.html"


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(View):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
        except (ValueError, stripe.error.SignatureVerificationError):
            return HttpResponseBadRequest("Firma de webhook inválida")

        services.handle_webhook_event(event)
        return HttpResponse(status=200)
