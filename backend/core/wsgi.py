"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from .settings.settings import DEBUG
from django.core.wsgi import get_wsgi_application

if DEBUG:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
    print("WSGI: Django loaded up in setting mode : Development")
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.production')
    print("WSGI: Django loaded up in setting mode : Production")

application = get_wsgi_application()
