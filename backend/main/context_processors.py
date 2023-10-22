from .models import Settings, Categories


def Default(request):
    return {
        'page_setting': Settings.objects.first(),
        'categories': Categories.objects.filter(is_active=True,level=0),
    }
