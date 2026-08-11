from django.conf import settings


def site_settings(request):
    return {
        "site_name": settings.SITE_NAME,
        "site_owner_name": settings.SITE_OWNER_NAME,
        "site_domain": settings.SITE_DOMAIN,
        "contact_email": settings.CONTACT_EMAIL,
        "legal_entity_name": settings.LEGAL_ENTITY_NAME,
        "legal_entity_rut": settings.LEGAL_ENTITY_RUT,
    }
