from .settings import *
import os

ALLOWED_HOSTS = ["*"]

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
CKEDITOR_UPLOAD_PATH = "uploads/"

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_ENDPOINT_SECRET_KEY = os.getenv("STRIPE_WEBHOOK_ENDPOINT_SECRET_KEY")
BASE_DOMAIN = os.getenv("BASE_DOMAIN")

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_password")
