import nested_admin
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .forms import PageAdminForm, ComponentsOnPageForm
from .models import Settings, Categories, Page, Seo, CustomerVideo, FAQ, ComponentsOnPage, Components, Ticket, \
    TicketCategory, TicketComment, TicketAttachment, ContactUs


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
    list_display = ["id", "user", "name", "is_active", "created_at", "updated_at"]


class TicketAttachmentInline(nested_admin.NestedTabularInline, ):
    model = TicketAttachment
    extra = 1


class TicketAttachmentAdmin(admin.ModelAdmin):
    list_display = ["id", "ticket", "comment", "file", "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at"]


class TicketCommentInline(nested_admin.NestedStackedInline, ):
    model = TicketComment
    inlines = [TicketAttachmentInline]
    extra = 1


class TicketAdmin(nested_admin.NestedModelAdmin):
    list_display = ["id", "author", "subject", "category", "status", "created_at", "updated_at"]
    list_filter = ["category", "status", "created_at"]
    inlines = [TicketCommentInline, TicketAttachmentInline]


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "is_check", "created_at", "updated_at"]
    list_filter = ["is_check", "created_at", "updated_at"]


admin.site.register(Settings)
admin.site.register(FAQ)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(CustomerVideo)
admin.site.register(Components)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketCategory)
admin.site.register(TicketAttachment, TicketAttachmentAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
