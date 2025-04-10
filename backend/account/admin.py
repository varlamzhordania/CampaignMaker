import nested_admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, UserBusinessProfile, BusinessAudience, UserIndustryAnswer, Industry, \
    IndustryQuestion
from .resources import UserResource, IndustryResource, IndustryQuestionResource


class BusinessAudienceInline(nested_admin.NestedStackedInline):
    model = BusinessAudience


class UserBusinessProfileInline(nested_admin.NestedStackedInline):
    model = UserBusinessProfile
    can_delete = True
    verbose_name_plural = 'Business Profile'
    inlines = [BusinessAudienceInline]


class UserIndustryAnswerInline(nested_admin.NestedStackedInline):
    model = UserIndustryAnswer
    can_delete = True
    verbose_name_plural = 'Industry Answer'
    extra = 0


class CustomUserAdmin(ImportExportModelAdmin, nested_admin.NestedModelAdmin, UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = (
        "id", "username", "email", "is_staff", "is_superuser", "show_questions", "is_active",
        "date_joined",
        "last_login")
    list_filter = ("is_staff", "is_active", "groups")
    readonly_fields = ("date_joined", "last_login", "last_ip")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Information",
         {"fields": ("first_name", "middle_name", "last_name", "email", "phone_number")}),
        ("Options", {"fields": ("show_questions",)}),
        ("Permissions",
         {"fields": ("is_staff", "is_superuser", "is_active", "groups", "user_permissions")}),
        ("Security", {"fields": ("date_joined", "last_login", "last_ip")}),
    )
    add_fieldsets = (
        (None, {
            "fields": (
                "username", "email", "password1", "password2",
                "groups", "is_staff", "is_active",
            )}
         ),
    )
    search_fields = ("id", "username", "email",)
    ordering = ("id",)
    resource_classes = [UserResource]
    inlines = (UserBusinessProfileInline, UserIndustryAnswerInline)


admin.site.register(User, CustomUserAdmin)


@admin.register(Industry)
class IndustryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'is_active', 'create_at', 'update_at']
    list_filter = ['is_active', 'create_at', 'update_at']
    search_fields = ['id', 'name']
    resource_classes = [IndustryResource]


@admin.register(IndustryQuestion)
class IndustryQuestionAdmin(ImportExportModelAdmin):
    list_display = ['id', 'industry', 'name', 'answer_type', 'question_order', 'optional',
                    'is_active', 'create_at', 'update_at']
    list_filter = ['optional', 'answer_type', 'is_active', 'create_at', 'update_at', 'industry']
    search_fields = ['id', 'name']
    resource_classes = [IndustryQuestionResource]
