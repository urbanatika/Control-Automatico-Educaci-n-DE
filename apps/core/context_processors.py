from django.conf import settings


def site_settings(request):
    return {
        "site_name": settings.SITE_NAME,
        "site_owner_name": settings.SITE_OWNER_NAME,
    }
