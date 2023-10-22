from django.contrib import admin
from .models import CampaignZip, CampaignAudio, CampaignSMS, CampaignType, CampaignSMSType, Campaign, CampaignEmail, \
    CampaignEmailType, CampaignEmailTemplate


# Register your models here.


class CampaignSMSInline(admin.StackedInline):
    model = CampaignSMS


class CampaignEmailInline(admin.StackedInline):
    model = CampaignEmail


class CampaignAudioInline(admin.StackedInline):
    model = CampaignAudio


class CampaignAdmin(admin.ModelAdmin):
    inlines = [CampaignSMSInline, CampaignEmailInline, CampaignAudioInline]
    list_display = ["id", "customer", "admin", "type", "status", "is_resubmit", "date_start"]
    list_filter = ["admin", "type", "status", "zips", "is_resubmit"]
    search_fields = ["id", "customer__username", "customer__email"]


admin.site.register(CampaignZip)
admin.site.register(CampaignType)
admin.site.register(CampaignSMSType)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(CampaignEmailType)
admin.site.register(CampaignEmailTemplate)
