from django.contrib import sitemaps
from django.urls import reverse
from .models import Categories


class HomeViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return ["main:home", ]

    def location(self, item):
        return reverse(item)


class CategoryViewSitemap(sitemaps.GenericSitemap):
    info_dict = {
        "queryset": Categories.objects.filter(is_active=True),
        "date_field": "create_at",
    }

    def __init__(self, priority=None, changefreq=None, protocol=None):
        info_dict = self.info_dict
        self.queryset = info_dict["queryset"]
        self.date_field = info_dict.get("date_field")
        self.priority = self.priority or priority
        self.changefreq = self.changefreq or changefreq
        self.protocol = self.protocol or protocol


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return ["main:about", "main:contact", "main:privacy", "main:terms", "main:refund"]

    def location(self, item):
        return reverse(item)
