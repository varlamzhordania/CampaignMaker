from django.contrib import admin
from .models import Settings, Categories, Page, Seo, CustomerVideo, FAQ, ComponentsOnPage, Components
from mptt.admin import MPTTModelAdmin
import nested_admin
from .forms import PageAdminForm, ComponentsOnPageForm


# Register your models here.
class SeoStackedInline(nested_admin.NestedStackedInline):
    model = Seo
    extra = 1
    max_num = 1


class ComponentsOnPageInline(nested_admin.NestedStackedInline):
    model = ComponentsOnPage
    form = ComponentsOnPageForm
    extra = 1
    max_num = 10


class PageStackedInline(nested_admin.NestedStackedInline, ):
    model = Page
    form = PageAdminForm
    inlines = [ComponentsOnPageInline, SeoStackedInline]
    extra = 1
    max_num = 1


class PageAdmin(nested_admin.NestedModelAdmin):
    inlines = [ComponentsOnPageInline, SeoStackedInline]
    list_display = ["id", "category", "type", ]
    list_filter = ["type"]


class CategoriesAdmin(MPTTModelAdmin, nested_admin.NestedModelAdmin):
    inlines = [PageStackedInline]


class ComponentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "name", "is_active", "create_at", "update_at"]


admin.site.register(Settings)
admin.site.register(FAQ)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(CustomerVideo)
admin.site.register(Components)
