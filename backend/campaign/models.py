from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import os
from pydub import AudioSegment
from .validators import validate_file_size, validate_file_extension, validate_file_duration
from datetime import datetime

# Create your models here.


CAMPAIGN_STATUS = (
    ("cancel", "Canceled"),
    ("wait", "Waiting for approval"),
    ("processing", "Processing"),
    ("complete", "Complete"),
)


class CampaignType(models.Model):
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
    is_active = models.BooleanField(verbose_name=_("Published"), default=False)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Create"))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("Date Modified"))

    class Meta:
        verbose_name = _("Campaign Type")
        verbose_name_plural = _("Campaign Types")

    def __str__(self):
        return self.name

    def get_full_info(self):
        return f"{self.name} - {self.price}"


class CampaignZip(models.Model):
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
    is_active = models.BooleanField(verbose_name=_("Published"), default=False)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Create"))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("Date Modified"))

    class Meta:
        verbose_name = _("Campaign Type")
        verbose_name_plural = _("Campaign Types")

    def __str__(self):
        return self.name

    def get_full_info(self):
        return f"{self.name} - {self.price}"


class Campaign(models.Model):
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
    zips = models.ManyToManyField(
        CampaignZip, verbose_name=_("Zips")
    )
    total = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Total Households"),
        help_text=_("format: required, cannot be 0 or negative number"),
        blank=False,
        null=False,
        validators=[MinValueValidator(int(1))],
    )
    status = models.CharField(
        max_length=31,
        choices=CAMPAIGN_STATUS,
        blank=False,
        null=False,
        default="wait",
        verbose_name=_("Status"),
    )
    date_start = models.DateTimeField(
        verbose_name=_("Date Start"),
        help_text=_("format: not required, daytime that campaign start"),
        blank=True,
        null=True,
    )
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Create"))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("Date Modified"))

    class Meta:
        verbose_name = _("Campaign")
        verbose_name_plural = _("Campaigns")

    def __str__(self):
        return self.id

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


class CampaignSMSType(models.Model):
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
    is_active = models.BooleanField(verbose_name=_("Published"), default=False)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Create"))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("Date Modified"))

    class Meta:
        verbose_name = _("SMS Type")
        verbose_name_plural = _("SMS Types")

    def __str__(self):
        return self.name


class CampaignSMS(models.Model):
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
    # is_active = models.BooleanField(verbose_name=_("Published"), default=False)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Create"))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("Date Modified"))

    class Meta:
        verbose_name = _("CampaignSMS")
        verbose_name_plural = _("CampaignSMSes")

    def __str__(self):
        return self.campaign


class CampaignEmailType(models.Model):
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
    is_active = models.BooleanField(verbose_name=_("Published"), default=False)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Create"))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("Date Modified"))

    class Meta:
        verbose_name = _("Email Type")
        verbose_name_plural = _("Email Types")

    def __str__(self):
        return self.name


class CampaignEmail(models.Model):
    campaign = models.OneToOneField(
        Campaign,
        verbose_name=_("Campaign"),
        related_name="campaign_email",
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        help_text=_("format: required, belonging campaign")
    )
    type = models.ForeignKey(
        CampaignSMSType,
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
    body = models.TextField(
        blank=False, null=False, verbose_name=_("Email Body")
    )
    # is_active = models.BooleanField(verbose_name=_("Published"), default=False)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Create"))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("Date Modified"))

    class Meta:
        verbose_name = _("CampaignEmail")
        verbose_name_plural = _("CampaignEmails")

    def __str__(self):
        return self.campaign


def generate_filename(instance, filename):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    extension = filename.split('.')[-1]
    return f"audio/audio_{timestamp}.{extension}"


class CampaignAudio(models.Model):
    campaign = models.OneToOneField(
        Campaign,
        verbose_name=_("Campaign"),
        related_name="campaign_audio",
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        help_text=_("format: required, belonging campaign")
    )
    file = models.FileField(
        upload_to=generate_filename,
        verbose_name=_("File"),
        help_text=_("format: Only .mp3, .m4a and .wav files are allowed."),
        validators=[
            validate_file_duration,
            validate_file_extension,
            validate_file_size
        ],
        blank=False,
        null=False,
    )
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Create"))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("Date Modified"))

    class Meta:
        verbose_name = _("CampaignAudio")
        verbose_name_plural = _("CampaignAudios")

    def __str__(self):
        return self.campaign
