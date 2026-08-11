import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-insecure-secret-key-change-me")
DEBUG = os.environ.get("DEBUG", "True") == "True"
ALLOWED_HOSTS = [h.strip() for h in os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h.strip()]

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
]

THIRD_PARTY_APPS = []

LOCAL_APPS = [
    "apps.accounts",
    "apps.core",
    "apps.courses",
    "apps.subscriptions",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "controlweb.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.site_settings",
                "apps.subscriptions.context_processors.subscription_status",
            ],
        },
    },
]

WSGI_APPLICATION = "controlweb.wsgi.application"
ASGI_APPLICATION = "controlweb.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "accounts:dashboard"
LOGOUT_REDIRECT_URL = "core:home"

# Marca / contenido del sitio
SITE_NAME = os.environ.get("SITE_NAME", "Diego Elorza | Control Automático")
SITE_OWNER_NAME = os.environ.get("SITE_OWNER_NAME", "Diego Elorza")
SITE_DOMAIN = os.environ.get("SITE_DOMAIN", "controlautomatico-app.azurewebsites.net")
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "diego@urbanatika.org")

# Identidad legal (usada en Términos y Condiciones / Política de Privacidad)
LEGAL_ENTITY_NAME = os.environ.get("LEGAL_ENTITY_NAME", "Urbanatika")
LEGAL_ENTITY_RUT = os.environ.get("LEGAL_ENTITY_RUT", "65.177.213-3")

# Formulario de contacto: a dónde se envían los mensajes del sitio.
CONTACT_FORM_RECIPIENT = os.environ.get("CONTACT_FORM_RECIPIENT", "contacto@urbanatika.org")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", f"{SITE_OWNER_NAME} <{CONTACT_EMAIL}>")

# Redes sociales de Diego Elorza (footer). Deja en blanco para ocultar un ícono.
SOCIAL_INSTAGRAM_URL = os.environ.get("SOCIAL_INSTAGRAM_URL", "https://www.instagram.com/diegoelorza/")
SOCIAL_LINKEDIN_URL = os.environ.get("SOCIAL_LINKEDIN_URL", "https://www.linkedin.com/in/diegoelorza/")
SOCIAL_YOUTUBE_URL = os.environ.get("SOCIAL_YOUTUBE_URL", "https://www.youtube.com/@urbanatika")
SOCIAL_X_URL = os.environ.get("SOCIAL_X_URL", "https://x.com/elorza_diego")

# Mercado Pago (usa credenciales de prueba primero — ver .env.example)
MERCADOPAGO_ACCESS_TOKEN = os.environ.get("MERCADOPAGO_ACCESS_TOKEN", "")
MERCADOPAGO_PUBLIC_KEY = os.environ.get("MERCADOPAGO_PUBLIC_KEY", "")
MERCADOPAGO_WEBHOOK_SECRET = os.environ.get("MERCADOPAGO_WEBHOOK_SECRET", "")
MERCADOPAGO_MONTHLY_AMOUNT_CLP = int(os.environ.get("MERCADOPAGO_MONTHLY_AMOUNT_CLP", "14990"))
MERCADOPAGO_ANNUAL_AMOUNT_CLP = int(os.environ.get("MERCADOPAGO_ANNUAL_AMOUNT_CLP", "119990"))
