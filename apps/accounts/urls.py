from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("registro/", views.SignupView.as_view(), name="signup"),
    path("registro/verifica-tu-correo/", views.VerifyEmailSentView.as_view(), name="verify_email_sent"),
    path("registro/verificar/<uidb64>/<token>/", views.VerifyEmailView.as_view(), name="verify_email"),
    path(
        "iniciar-sesion/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("cerrar-sesion/", auth_views.LogoutView.as_view(), name="logout"),
    path("mi-cuenta/", views.DashboardView.as_view(), name="dashboard"),
    path(
        "clave/cambiar/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/password_change.html",
            success_url="/cuenta/mi-cuenta/",
        ),
        name="password_change",
    ),
    path(
        "clave/olvide/",
        auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
        name="password_reset",
    ),
    path(
        "clave/olvide/enviado/",
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "clave/restablecer/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    path(
        "clave/restablecer/listo/",
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]
