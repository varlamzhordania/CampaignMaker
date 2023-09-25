from .models import Settings


def Default(request):
    return {
        'page_setting': Settings.objects.first()
    }
