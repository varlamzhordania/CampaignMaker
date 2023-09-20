from .settings import *

ALLOWED_HOSTS = ["*"]

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STRIPE_SECRET_KEY = 'sk_test_51MrHupIOqCK98Pr5qzuQ2eAh5r7ksf2LPgMnKkDZBJLQznuRaxFWOzRYlA2RMLWLhII34v0pmOZvQZUIlro5sgrf00CNyBJpG8'
STRIPE_WEBHOOK_ENDPOINT_SECRET_KEY = 'whsec_96a4e0d27b3c38f4ecf5d97657f443fd4b5e95c002a8cfc4a74a294414d5f833'
STRIPE_BASE_DOMAIN = 'http://127.0.0.1:8000'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]
