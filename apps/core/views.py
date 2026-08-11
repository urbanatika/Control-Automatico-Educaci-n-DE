from smtplib import SMTPException

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from apps.courses.models import Track

from .forms import ContactForm


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tracks"] = Track.objects.prefetch_related("courses")[:7]
        return context


class AboutView(TemplateView):
    template_name = "core/about.html"


class TermsView(TemplateView):
    template_name = "core/terms.html"


class PrivacyView(TemplateView):
    template_name = "core/privacy.html"


class ContactView(FormView):
    template_name = "core/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("core:contact")

    def form_valid(self, form):
        try:
            EmailMessage(
                subject=f"[{settings.SITE_NAME}] {form.cleaned_data['subject']}",
                body=(
                    f"Nombre: {form.cleaned_data['name']}\n"
                    f"Correo: {form.cleaned_data['email']}\n\n"
                    f"{form.cleaned_data['message']}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_FORM_RECIPIENT],
                reply_to=[form.cleaned_data["email"]],
            ).send(fail_silently=False)
        except (OSError, SMTPException):
            messages.error(
                self.request,
                "No se pudo enviar tu mensaje por un problema técnico. "
                f"Escríbenos directamente a {settings.CONTACT_FORM_RECIPIENT}.",
            )
            return super().form_valid(form)

        messages.success(self.request, "Tu mensaje fue enviado. Te responderemos a la brevedad.")
        return super().form_valid(form)
