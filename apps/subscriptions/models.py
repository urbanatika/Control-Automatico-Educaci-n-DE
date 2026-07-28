from django.conf import settings
from django.db import models
from django.utils import timezone


class Subscription(models.Model):
    class Plan(models.TextChoices):
        MONTHLY = "monthly", "Mensual"
        ANNUAL = "annual", "Anual"

    class Status(models.TextChoices):
        INCOMPLETE = "incomplete", "Incompleta"
        TRIALING = "trialing", "En prueba"
        ACTIVE = "active", "Activa"
        PAST_DUE = "past_due", "Pago pendiente"
        CANCELED = "canceled", "Cancelada"
        UNPAID = "unpaid", "Impaga"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscription", verbose_name="usuario"
    )
    plan = models.CharField("plan", max_length=20, choices=Plan.choices, default=Plan.MONTHLY)
    status = models.CharField("estado", max_length=20, choices=Status.choices, default=Status.INCOMPLETE)
    stripe_customer_id = models.CharField("ID cliente Stripe", max_length=255, blank=True)
    stripe_subscription_id = models.CharField("ID suscripción Stripe", max_length=255, blank=True)
    current_period_end = models.DateTimeField("fin del período actual", null=True, blank=True)
    created_at = models.DateTimeField("creada", auto_now_add=True)
    updated_at = models.DateTimeField("actualizada", auto_now=True)

    class Meta:
        verbose_name = "suscripción"
        verbose_name_plural = "suscripciones"

    def __str__(self):
        return f"{self.user} — {self.get_status_display()}"

    @property
    def is_active(self) -> bool:
        if self.status not in (self.Status.ACTIVE, self.Status.TRIALING):
            return False
        if self.current_period_end and self.current_period_end < timezone.now():
            return False
        return True
