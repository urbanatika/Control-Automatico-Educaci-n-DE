from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("sobre-mi/", views.AboutView.as_view(), name="about"),
    path("legal/terminos-y-condiciones/", views.TermsView.as_view(), name="terms"),
    path("legal/privacidad/", views.PrivacyView.as_view(), name="privacy"),
]
