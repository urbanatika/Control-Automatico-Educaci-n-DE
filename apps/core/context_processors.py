from django.conf import settings


def site_settings(request):
    return {
        "site_name": settings.SITE_NAME,
        "site_owner_name": settings.SITE_OWNER_NAME,
        "site_domain": settings.SITE_DOMAIN,
        "contact_email": settings.CONTACT_EMAIL,
        "contact_form_recipient": settings.CONTACT_FORM_RECIPIENT,
        "google_contact_form_id": settings.GOOGLE_CONTACT_FORM_ID,
        "google_contact_form_field_name": settings.GOOGLE_CONTACT_FORM_FIELD_NAME,
        "google_contact_form_field_email": settings.GOOGLE_CONTACT_FORM_FIELD_EMAIL,
        "google_contact_form_field_phone": settings.GOOGLE_CONTACT_FORM_FIELD_PHONE,
        "google_contact_form_field_message": settings.GOOGLE_CONTACT_FORM_FIELD_MESSAGE,
        "legal_entity_name": settings.LEGAL_ENTITY_NAME,
        "legal_entity_rut": settings.LEGAL_ENTITY_RUT,
        "social_instagram_url": settings.SOCIAL_INSTAGRAM_URL,
        "social_linkedin_url": settings.SOCIAL_LINKEDIN_URL,
        "social_youtube_url": settings.SOCIAL_YOUTUBE_URL,
        "social_x_url": settings.SOCIAL_X_URL,
    }
