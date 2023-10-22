from django import template
from django.contrib.auth.models import Group
import requests
from django.conf import settings
from django.utils.safestring import mark_safe
from django.core.cache import cache

domain = settings.BASE_DOMAIN

register = template.Library()


@register.filter("has_group")
def has_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return False

    return group in user.groups.all() or user.is_staff or user.is_superuser


@register.simple_tag()
def load_content_from_url(url):
    cache_content = cache.get(url)
    if cache_content is not None:
        print("cached")
        return cache_content

    try:
        response = requests.get(domain + url)
        if response.status_code == 200:
            return mark_safe(response.text)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    return "Failed to load content"
