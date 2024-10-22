import os

from .settings import *

ALLOWED_HOSTS = ["*"]

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
CKEDITOR_UPLOAD_PATH = "uploads/"

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_ENDPOINT_SECRET_KEY = os.getenv("STRIPE_WEBHOOK_ENDPOINT_SECRET_KEY")
BASE_DOMAIN = os.getenv("BASE_DOMAIN")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("DB_NAME", "campaignMakerDB"),
        'USER': os.getenv("DB_USER", "campaignMakerAdmin"),
        'PASSWORD': os.getenv("DB_PASSWORD", "aRZXFK0VVNtW817"),
        'HOST': "postgres",  # Use the service name from docker-compose.yml
        'PORT': '5432',
    }
}

CACHES = {
    'default': {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        'LOCATION': os.getenv("REDIS_HOST"),  # Use the REDIS_HOST environment variable
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_password")
