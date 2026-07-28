from django.urls import path

from . import views

app_name = "subscriptions"

urlpatterns = [
    path("", views.PricingView.as_view(), name="pricing"),
    path("checkout/", views.CreateCheckoutSessionView.as_view(), name="checkout"),
    path("cancelar/", views.UnsubscribeConfirmView.as_view(), name="unsubscribe_confirm"),
    path("cancelar/confirmar/", views.UnsubscribeView.as_view(), name="unsubscribe"),
    path("exito/", views.SuccessView.as_view(), name="success"),
    path("webhook/", views.MercadoPagoWebhookView.as_view(), name="webhook"),
]
