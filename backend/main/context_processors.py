from .models import Settings, Categories
from django.conf import settings


def Default(request):
    return {
        'page_setting': Settings.objects.first(),
        'categories': Categories.objects.filter(is_active=True, level=0),
        'asset_version': settings.STATIC_VERSION
    }
