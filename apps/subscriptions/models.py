from django.conf import settings
from django.db import models


class Subscription(models.Model):
    class Plan(models.TextChoices):
        MONTHLY = "monthly", "Mensual"
        ANNUAL = "annual", "Anual"

    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente de autorización"
        AUTHORIZED = "authorized", "Activa"
        PAUSED = "paused", "Pausada"
        CANCELLED = "cancelled", "Cancelada"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscription", verbose_name="usuario"
    )
    plan = models.CharField("plan", max_length=20, choices=Plan.choices, default=Plan.MONTHLY)
    status = models.CharField("estado", max_length=20, choices=Status.choices, default=Status.PENDING)
    mercadopago_preapproval_id = models.CharField("ID de suscripción en Mercado Pago", max_length=255, blank=True)
    mercadopago_payer_email = models.EmailField("correo del pagador en Mercado Pago", blank=True)
    next_payment_date = models.DateTimeField("próximo cobro", null=True, blank=True)
    created_at = models.DateTimeField("creada", auto_now_add=True)
    updated_at = models.DateTimeField("actualizada", auto_now=True)

    class Meta:
        verbose_name = "suscripción"
        verbose_name_plural = "suscripciones"

    def __str__(self):
        return f"{self.user} — {self.get_status_display()}"

    @property
    def is_active(self) -> bool:
        return self.status == self.Status.AUTHORIZED
