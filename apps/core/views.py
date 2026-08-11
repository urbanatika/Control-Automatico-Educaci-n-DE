from django.views.generic import TemplateView

from apps.courses.models import Track


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
