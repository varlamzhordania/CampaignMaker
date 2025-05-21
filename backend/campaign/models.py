from decimal import Decimal
from datetime import time

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, FileExtensionValidator
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.template import Template, Context
from django_ckeditor_5.fields import CKEditor5Field
from autoslug import AutoSlugField

from main.models import Settings
from core.models import BaseModel, UploadPath

from .validators import (
    validate_file_duration,
    FileSizeValidator,
)


class CampaignEmailTemplate(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        blank=False,
        null=False,
        unique=False,
        help_text=_("format: required, max-255 character, name of your Email Template")
    )
    template = models.FileField(
        upload_to=UploadPath("templates", "email"),
        blank=False,
        null=False,
        validators=[FileExtensionValidator(allowed_extensions=["html", "htm"])],
        verbose_name=_("Template"),
        help_text=_("format: only .html .htm are allowed"),
    )
    thumbnail = models.ImageField(
        upload_to=UploadPath("images", "thumbnail"),
        blank=False,
        null=False,
        verbose_name=_("Template Thumbnail"),
        help_text=_("format: JPEG,JPG,PNG,SVG,WEBP")
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        unique=False,
        null=True,
        default=0,
        blank=True,
        verbose_name=_("Template Price"),
        help_text=_("format: default-0,  considered for future improvements"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    slug = AutoSlugField(
        allow_unicode=True,
        populate_from="name",
        editable=True,
        unique=True,
        verbose_name=_("Safe URL"),
        blank=True,
        null=False
    )

    class Meta:
        verbose_name = _("Email Template")
        verbose_name_plural = _("Email templates")

    def get_rendered_content(self, context):
        template_content = ''
        with self.template.open('r') as file:
            template_content = file.read()
        template = Template(template_content)
        rendered_content = template.render(Context(context, autoescape=False))
        return rendered_content


class CampaignType(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        blank=False,
        null=False,
        unique=False,
        help_text=_("format: required, max-255 character, name of your campaign")
    )
    slug = AutoSlugField(
        allow_unicode=True,
        populate_from="name",
        editable=True,
        unique=True,
        verbose_name=_("Safe URL"),
        blank=True,
        null=False
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        unique=False,
        null=False,
        blank=False,
        verbose_name=_("Price"),
        help_text=_("format: maximum price 99999999.99"),
        validators=[MinValueValidator(Decimal("0.01"))]
    )

    class Meta:
        verbose_name = _("Campaign Type")
        verbose_name_plural = _("Campaign Types")

    def __str__(self):
        return self.name

    def get_full_info(self):
        return f"{self.name} - {self.price}"


class CampaignZip(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        blank=False,
        null=False,
        unique=False,
        help_text=_("format: required, max-255 character, name of your campaign")
    )
    slug = AutoSlugField(
        allow_unicode=True,
        populate_from="name",
        editable=True,
        unique=True,
        verbose_name=_("Safe URL"),
        blank=True,
        null=False
    )
    code = models.CharField(
        max_length=16,
        verbose_name=_("Code"),
        blank=False,
        null=False,
        unique=False,
        help_text=_("format: required, max-16")
    )
    timezone_offset = models.CharField(
        max_length=6,
        verbose_name=_("Timezone Offset"),
        default="UTC",
        help_text=_("Timezone offset for the zip code (e.g. -05:00, +02:00, etc.)")
    )

    timezone_name = models.CharField(
        max_length=63,
        verbose_name=_("Timezone Name"),
        default="UTC",
        help_text=_("Full name of the timezone (e.g. 'America/New_York', 'Europe/London')")
    )

    class Meta:
        verbose_name = _("Campaign Zip")
        verbose_name_plural = _("Campaign Zips")

    def __str__(self):
        return self.name

    def get_full_info(self):
        return f"{self.name} - {self.price}"


class Campaign(BaseModel):
    class StatusChoices(models.TextChoices):
        CANCEL = "cancel", _("Canceled"),
        PAYMENT = "payment", _("Waiting for payment")
        DISAPPROVED = "disapprove", _("Disapproved")
        WAITING = "wait", _("Waiting for approval")
        PROCESSING = "processing", _("Processing")
        COMPLETED = "complete", _("Completed")

    customer = models.ForeignKey(
        get_user_model(),
        verbose_name=_("Customer"),
        related_name="campaign_customer",
        on_delete=models.PROTECT,
        blank=False, null=False,
        help_text=_("format: required")
    )
    admin = models.ForeignKey(
        get_user_model(),
        verbose_name=_("Last Admin"),
        related_name="campaign_admin",
        on_delete=models.SET_NULL,
        blank=True, null=True,
        help_text=_("format: last admin that changed campaign")
    )
    type = models.ForeignKey(
        CampaignType,
        verbose_name=_("Campaign Type"),
        related_name="campaign_type",
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        help_text=_("format: required")
    )
    email_template = models.ForeignKey(
        CampaignEmailTemplate,
        verbose_name=_("Email Template"),
        related_name="campaign_email_template",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    zips = models.ManyToManyField(
        CampaignZip, verbose_name=_("Zips")
    )
    status = models.CharField(
        max_length=31,
        choices=StatusChoices.choices,
        blank=False,
        null=False,
        default=StatusChoices.PAYMENT,
        verbose_name=_("Status"),
    )
    note = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Admin Note"),
        help_text=_("format: it will be shown to user when disapproved")
    )
    date_start = models.DateTimeField(
        verbose_name=_("Date Start"),
        help_text=_("format: not required, daytime that campaign start"),
        blank=True,
        null=True,
    )
    is_resubmit = models.BooleanField(
        default=False,
        verbose_name=_("Is Resubmitted"),
        help_text=_(
            "format: default false , if false allow user to resubmit if status is equal to disapprove"
        ),
    )
    is_active = None

    class Meta:
        verbose_name = _("Campaign")
        verbose_name_plural = _("Campaigns")
        ordering = ["-id"]

    def __str__(self):
        return str(self.id)

    def get_sms(self):
        queryset = CampaignSMS.objects.filter(campaign_id=self.id)
        if queryset.count() > 0:
            return queryset.first()
        else:
            return None

    def get_email(self):
        queryset = CampaignEmail.objects.filter(campaign_id=self.id)
        if queryset.count() > 0:
            return queryset.first()
        else:
            return None

    def get_audio(self):
        queryset = CampaignAudio.objects.filter(campaign_id=self.id)
        if queryset.count() > 0:
            return queryset.first()
        else:
            return None

    def get_price(self):
        price = 0
        price += self.type.price
        if self.campaign_audio.text:
            price += Settings.objects.first().audio_price
        return price

    def get_days_difference(self):
        today = timezone.now()
        difference = today.date() - self.create_at.date()
        return difference.days


class CampaignSMSType(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        blank=False,
        null=False,
        unique=False,
        help_text=_("format: required, max-255 character, name of your SMS type")
    )
    slug = AutoSlugField(
        allow_unicode=True,
        populate_from="name",
        editable=True,
        unique=True,
        verbose_name=_("Safe URL"),
        blank=True,
        null=False
    )

    class Meta:
        verbose_name = _("SMS Type")
        verbose_name_plural = _("SMS Types")

    def __str__(self):
        return self.name


class CampaignSMS(BaseModel):
    campaign = models.OneToOneField(
        Campaign,
        verbose_name=_("Campaign"),
        related_name="campaign_sms",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        help_text=_("format: required, belonging campaign")
    )
    type = models.ForeignKey(
        CampaignSMSType,
        verbose_name=_("Salutation Type"),
        related_name="campaignSMS_type",
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        help_text=_("format: required, SMS type")
    )
    body = models.TextField(
        blank=False, null=False, verbose_name=_("SMS Body")
    )
    is_active = None

    class Meta:
        verbose_name = _("CampaignSMS")
        verbose_name_plural = _("CampaignSMSes")

    def __str__(self):
        return self.campaign.__str__()


class CampaignEmailType(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        blank=False,
        null=False,
        unique=False,
        help_text=_("format: required, max-255 character, name of your Email type")
    )
    slug = AutoSlugField(
        allow_unicode=True,
        populate_from="name",
        editable=True,
        unique=True,
        verbose_name=_("Safe URL"),
        blank=True,
        null=False
    )

    class Meta:
        verbose_name = _("Email Type")
        verbose_name_plural = _("Email Types")

    def __str__(self):
        return self.name


class CampaignEmail(BaseModel):
    campaign = models.OneToOneField(
        Campaign,
        verbose_name=_("Campaign"),
        related_name="campaign_email",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        help_text=_("format: required, belonging campaign")
    )
    type = models.ForeignKey(
        CampaignEmailType,
        verbose_name=_("Salutation Type"),
        related_name="campaignEmail_type",
        blank=False,
        on_delete=models.PROTECT,
        null=False,
        help_text=_("format: required, Email type")
    )
    subject = models.CharField(
        max_length=255,
        verbose_name=_("Email Subject"),
        blank=False,
        null=False,
        help_text=_("format: required, max-255 character")
    )
    body = CKEditor5Field(
        blank=False, null=False, verbose_name=_("Email Body")
    )
    is_active = None

    class Meta:
        verbose_name = _("CampaignEmail")
        verbose_name_plural = _("CampaignEmails")

    def __str__(self):
        return self.campaign.__str__()


class CampaignAudio(BaseModel):
    campaign = models.OneToOneField(
        Campaign,
        verbose_name=_("Campaign"),
        related_name="campaign_audio",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        help_text=_("format: required, belonging campaign")
    )
    text = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Text"),
        help_text=_("format: the text that user want to convert to audio")
    )
    file = models.FileField(
        upload_to=UploadPath("uploads", "audio"),
        verbose_name=_("File"),
        help_text=_("format: Only .mp3, .m4a and .wav files are allowed."),
        validators=[
            FileExtensionValidator(allowed_extensions=['mp3', 'm4a', 'wav']),
            FileSizeValidator(max_size_mb=20),
            validate_file_duration,
        ],
        blank=True,
        null=True,
    )
    is_active = None

    class Meta:
        verbose_name = _("CampaignAudio")
        verbose_name_plural = _("CampaignAudios")

    def __str__(self):
        return self.campaign.__str__()


class SocialMedia(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        blank=False,
        null=False,
        unique=True,
        help_text=_("format: required, max-255 character")
    )
    slug = AutoSlugField(
        verbose_name=_("slug"),
        populate_from="name",
        editable=True,
        unique=True,
        help_text=_("format: required, max-255 character")
    )
    object_name = models.CharField(
        max_length=255,
        verbose_name=_("Object Name"),
        blank=False,
        null=False,
        help_text=_(
            "format: required, max-255 character, this name will be used to when sending the data, example: 'facebook':{}"
        )
    )
    tutorial_video = models.FileField(
        verbose_name=_("Tutorial Video"),
        upload_to=UploadPath("uploads", "video"),
        validators=[
            FileExtensionValidator(allowed_extensions=["mp4", "webm", 'ogg', 'mkv']),
        ],
        blank=True,
        null=True,
        help_text=_("Optional file for a tutorial video on how to fill this form")
    )
    manual_guide = models.TextField(
        verbose_name=_("Manual Guide"),
        blank=True,
        null=True,
        help_text=_("Optional step-by-step guide for users on how to complete the form")
    )

    class Meta:
        verbose_name = _("Social Media")
        verbose_name_plural = _("Social Medias")
        ordering = ("name",)
        unique_together = ("name", "object_name")

    def __str__(self):
        return self.name


class SocialMediaFields(BaseModel):
    social_media = models.ForeignKey(
        SocialMedia,
        verbose_name=_("Social Media"),
        related_name="social_media_fields",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Field Name"),
        blank=False,
        null=False,
        help_text=_("format: required, max-255 character, example: username, password...etc")
    )
    object_name = models.CharField(
        max_length=255,
        verbose_name=_("Object Name"),
        blank=False,
        null=False,
        help_text=_(
            "format: required, max-255 character, this name will be used to when sending the data, example: 'username':''}"
        )
    )
    is_optional = models.BooleanField(
        default=False,
        verbose_name=_("Optional"),
    )

    class Meta:
        verbose_name = _("Social Media Fields")
        verbose_name_plural = _("Social Media Fields")
        ordering = ("social_media", "name",)
        unique_together = ("social_media", "name", "object_name")

    def __str__(self):
        return f"{self.social_media.name} : {self.name}"


class SocialMediaUploads(BaseModel):
    social_media = models.ForeignKey(
        SocialMedia,
        verbose_name=_("Social Media"),
        related_name="social_media_uploads",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Field Name"),
        blank=False,
        null=False,
        help_text=_("format: required, max-255 character, example: username, password...etc")
    )
    object_name = models.CharField(
        max_length=255,
        verbose_name=_("Object Name"),
        blank=False,
        null=False,
        help_text=_(
            "format: required, max-255 character, this name will be used to when sending the data, example: 'logo':''}"
        )
    )
    is_optional = models.BooleanField(
        default=False,
        verbose_name=_("Optional"),
    )

    class Meta:
        verbose_name = _("Social Media Upload")
        verbose_name_plural = _("Social Media Uploads")
        ordering = ("social_media", "name",)
        unique_together = ("social_media", "name", "object_name")

    def __str__(self):
        return f"{self.social_media.name} : {self.name}"


class SocialMediaAccounts(BaseModel):
    social_media = models.ForeignKey(
        SocialMedia,
        verbose_name=_("Social Media"),
        related_name="social_media_accounts",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    username = models.CharField(
        max_length=255,
        verbose_name=_("Username"),
        blank=False,
        null=False,
        help_text=_(
            "format: required, max-255 character, this can contain email,phone or any other type of social media identifier"
        )
    )

    class Meta:
        verbose_name = _("Social Media Accounts")
        verbose_name_plural = _("Social Media Accounts")
        ordering = ("social_media", "username",)

    def __str__(self):
        return f"{self.social_media.name} : {self.username}"


class CampaignSocialMediaEntry(BaseModel):
    class FrequencyChoices(models.TextChoices):
        DAILY = "daily", _("Daily")
        TWO_DAY = "2_day", _("2-Day")
        THREE_DAY = "3_day", _("3-Day")
        WEEKLY = "weekly", _("Weekly")

    campaign = models.ForeignKey(
        Campaign,
        verbose_name=_("Campaign"),
        related_name="campaign_social_media_entry",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        help_text=_("format: required, belonging campaign")
    )
    social_media = models.ForeignKey(
        SocialMedia,
        verbose_name=_("Social Media"),
        related_name="entries",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    post_frequency = models.CharField(
        max_length=20,
        verbose_name=_("Post Frequency"),
        choices=FrequencyChoices.choices,
        default=FrequencyChoices.DAILY,
        blank=True,
        null=True,
        help_text=_("Frequency of social media posting")
    )
    post_time = models.TimeField(
        verbose_name=_("Post Time"),
        default=time(21, 0),  # 9:00 PM
        blank=True,
        null=True,
        help_text=_("Post time of social media posting")
    )

    is_active = None

    class Meta:
        verbose_name = _("Campaign Social Media Entry")
        verbose_name_plural = _("Campaign Social Media Entries")

    def __str__(self):
        return f"campaign: {self.campaign.id} - {self.social_media.name} entry #{self.pk}"


class CampaignSocialMediaFieldValue(BaseModel):
    entry = models.ForeignKey(
        CampaignSocialMediaEntry,
        verbose_name=_("Entry"),
        related_name="field_values",
        on_delete=models.CASCADE
    )
    field = models.ForeignKey(
        SocialMediaFields,
        verbose_name=_("Field"),
        related_name="entry_field_values",
        on_delete=models.CASCADE
    )
    value = models.CharField(
        max_length=1024,
        verbose_name=_("Value"),
        help_text=_("Value for this field, e.g. username or password")
    )
    is_active = None

    class Meta:
        verbose_name = _("Social Media Field Value")
        verbose_name_plural = _("Social Media Field Values")
        unique_together = ('entry', 'field')

    def __str__(self):
        return f"{self.entry} - {self.field.name}: {self.value}"


class CampaignSocialMediaUploadFile(BaseModel):
    entry = models.ForeignKey(
        CampaignSocialMediaEntry,
        verbose_name=_("Entry"),
        related_name="upload_files",
        on_delete=models.CASCADE
    )
    upload = models.ForeignKey(
        SocialMediaUploads,
        verbose_name=_("Field"),
        related_name="entry_uploads_files",
        on_delete=models.CASCADE
    )
    file = models.FileField(
        verbose_name=_("Value"),
        upload_to=UploadPath("uploads", "socials"),
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpeg", "jpg", "png", "mp4", "mov", "avi", "webm"]
            ),
            FileSizeValidator(max_size_mb=5),
        ],
    )
    is_active = None

    class Meta:
        verbose_name = _("Social Media Upload File")
        verbose_name_plural = _("Social Media Upload Files")
        unique_together = ('entry', 'upload')

    def __str__(self):
        return f"{self.entry} - {self.upload.name}: {self.file.url}"
