from django.contrib import admin

from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ["user", "plan", "status", "next_payment_date", "updated_at"]
    list_filter = ["plan", "status"]
    search_fields = ["user__email", "mercadopago_preapproval_id", "mercadopago_payer_email"]
    readonly_fields = ["mercadopago_preapproval_id", "mercadopago_payer_email", "created_at", "updated_at"]
