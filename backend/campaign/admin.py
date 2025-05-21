from django.contrib import admin
from .models import (
    CampaignZip, CampaignAudio, CampaignSMS, CampaignType, CampaignSMSType,
    Campaign, CampaignEmail,
    CampaignEmailType, CampaignEmailTemplate, SocialMedia, SocialMediaFields,
    CampaignSocialMediaEntry, CampaignSocialMediaFieldValue, SocialMediaAccounts,
    SocialMediaUploads, CampaignSocialMediaUploadFile,
)

from nested_admin import NestedStackedInline, NestedModelAdmin


class SocialMediaFieldsInline(admin.TabularInline):
    model = SocialMediaFields
    extra = 0
    fieldsets = (
        (None, {'fields': ('social_media', 'name', 'object_name', 'is_optional', 'is_active')}),
    )


class SocialMediaUploadsInline(admin.TabularInline):
    model = SocialMediaUploads
    extra = 0
    fieldsets = (
        (None, {'fields': ('social_media', 'name', 'object_name', 'is_optional', 'is_active')}),
    )


class SocialMediaAccountsInline(admin.TabularInline):
    model = SocialMediaAccounts
    extra = 0
    fieldsets = (
        (None, {'fields': ('social_media', 'username', 'is_active')}),
    )


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'object_name', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['name', 'slug', 'object_name']
    inlines = [SocialMediaFieldsInline, SocialMediaUploadsInline, SocialMediaAccountsInline]
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {'fields': ('name', 'object_name', 'is_active', 'created_at', 'updated_at')}),
        ('Guide', {'fields': ('tutorial_video', 'manual_guide',)}),
    )


class CampaignSocialMediaFieldValueInline(NestedStackedInline):
    model = CampaignSocialMediaFieldValue
    extra = 0


class CampaignSocialMediaUploadFileInline(NestedStackedInline):
    model = CampaignSocialMediaUploadFile
    extra = 0


class CampaignSocialMediaEntryStackedInline(NestedStackedInline):
    model = CampaignSocialMediaEntry
    inlines = [CampaignSocialMediaFieldValueInline, CampaignSocialMediaUploadFileInline]
    extra = 0


class CampaignSMSInline(NestedStackedInline):
    model = CampaignSMS


class CampaignEmailInline(NestedStackedInline):
    model = CampaignEmail


class CampaignAudioInline(NestedStackedInline):
    model = CampaignAudio


@admin.register(Campaign)
class CampaignAdmin(NestedModelAdmin, admin.ModelAdmin):
    inlines = [CampaignSMSInline, CampaignEmailInline, CampaignAudioInline,
               CampaignSocialMediaEntryStackedInline]
    list_display = ["id", "customer", "admin", "type", "status", "is_resubmit", "date_start"]
    list_filter = ["admin", "type", "status", "zips", "is_resubmit"]
    search_fields = ["id", "customer__username", "customer__email"]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CampaignZip)
class CampaignZipAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'timezone_name', 'timezone_offset', 'is_active',
                    'created_at',
                    'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CampaignType)
class CampaignTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'price', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['id', 'name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CampaignSMSType)
class CampaignSMSTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['id', 'name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CampaignEmailType)
class CampaignEmailTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['id', 'name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CampaignEmailTemplate)
class CampaignEmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'price', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['id', 'name']
    readonly_fields = ['created_at', 'updated_at']
