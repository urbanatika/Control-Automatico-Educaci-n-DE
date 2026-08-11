from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.courses.models import Course


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"

    def items(self):
        return [
            "core:home",
            "core:about",
            "courses:catalog",
            "subscriptions:pricing",
            "core:terms",
            "core:privacy",
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == "core:home" else 0.6


class CourseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Course.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return obj.get_absolute_url()
