from .settings import *
import os

ALLOWED_HOSTS = ["*"]

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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
