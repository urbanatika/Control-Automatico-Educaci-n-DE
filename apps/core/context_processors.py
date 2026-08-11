from django.conf import settings


def site_settings(request):
    return {
        "site_name": settings.SITE_NAME,
        "site_owner_name": settings.SITE_OWNER_NAME,
        "site_domain": settings.SITE_DOMAIN,
        "contact_email": settings.CONTACT_EMAIL,
        "contact_form_recipient": settings.CONTACT_FORM_RECIPIENT,
        "legal_entity_name": settings.LEGAL_ENTITY_NAME,
        "legal_entity_rut": settings.LEGAL_ENTITY_RUT,
        "social_instagram_url": settings.SOCIAL_INSTAGRAM_URL,
        "social_linkedin_url": settings.SOCIAL_LINKEDIN_URL,
        "social_youtube_url": settings.SOCIAL_YOUTUBE_URL,
        "social_x_url": settings.SOCIAL_X_URL,
    }
