from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import CreateView, TemplateView

from apps.courses.models import Track

from .forms import SignupForm
from .models import User


def send_verification_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    link = request.build_absolute_uri(reverse("accounts:verify_email", kwargs={"uidb64": uid, "token": token}))
    body = render_to_string(
        "accounts/verification_email.txt",
        {"user": user, "link": link, "site_name": settings.SITE_NAME},
    )
    send_mail(
        subject=f"Confirma tu cuenta en {settings.SITE_NAME}",
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:verify_email_sent")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()
        send_verification_email(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())


class VerifyEmailSentView(TemplateView):
    template_name = "accounts/verify_email_sent.html"


class VerifyEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save(update_fields=["is_active"])
            login(request, user)
            messages.success(request, "Tu cuenta fue confirmada. ¡Bienvenido/a!")
            return redirect("accounts:dashboard")

        messages.error(
            request,
            "El enlace de confirmación no es válido o ya expiró. Crea una cuenta nuevamente para recibir uno nuevo.",
        )
        return redirect("accounts:signup")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tracks"] = Track.objects.prefetch_related("courses").all()
        context["subscription"] = getattr(self.request.user, "subscription", None)
        return context
