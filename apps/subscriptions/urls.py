from django.urls import path

from . import views

app_name = "subscriptions"

urlpatterns = [
    path("", views.PricingView.as_view(), name="pricing"),
    path("checkout/", views.CreateCheckoutSessionView.as_view(), name="checkout"),
    path("portal/", views.BillingPortalView.as_view(), name="portal"),
    path("exito/", views.SuccessView.as_view(), name="success"),
    path("cancelado/", views.CancelView.as_view(), name="cancel"),
    path("webhook/", views.StripeWebhookView.as_view(), name="webhook"),
]
