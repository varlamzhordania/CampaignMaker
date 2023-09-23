import os

from .settings import *

ALLOWED_HOSTS = ["<your_domain>"]

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_ENDPOINT_SECRET_KEY = os.getenv("STRIPE_WEBHOOK_ENDPOINT_SECRET_KEY")
STRIPE_BASE_DOMAIN = os.getenv("STRIPE_BASE_DOMAIN")

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    }
}
