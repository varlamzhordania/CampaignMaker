from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import os
from .validators import validate_file_size, validate_file_extension, validate_file_duration
from datetime import datetime
from django.utils import timezone
from django.template import Template, Context
from django.template.loader import render_to_string
from ckeditor.fields import RichTextField

# Create your models here.


CAMPAIGN_STATUS = (
    ("cancel", "Canceled"),
    ("payment", "Waiting for payment"),
    ("disapproved", "Disapproved"),
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
        verbose_name = _("Campaign Zip")
        verbose_name_plural = _("Campaign Zips")

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
    status = models.CharField(
        max_length=31,
        choices=CAMPAIGN_STATUS,
        blank=False,
        null=False,
        default="payment",
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
        help_text=_("format: default false , if false allow user to resubmit if status is equal to disapprove"),
    )
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Create"))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("Date Modified"))

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
        return self.campaign.__str__()


def get_template_upload_path(instance, filename):
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    return f'email_templates/{timestamp}.html'


def validate_template_format(value):
    valid_extensions = ['.html', '.htm', 'html', 'htm']
    ext = value.name.lower().split('.')[-1]
    if ext not in valid_extensions:
        raise ValidationError(f'Invalid file format. Only {", ".join(valid_extensions)} files are allowed.')


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
    template = models.FileField(
        upload_to=get_template_upload_path,
        blank=True,
        null=True,
        validators=[validate_template_format],
        verbose_name=_("Template"),
        help_text=_("format: only .html .htm are allowed"),
    )
    is_active = models.BooleanField(verbose_name=_("Published"), default=False)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Create"))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("Date Modified"))

    class Meta:
        verbose_name = _("Email Type")
        verbose_name_plural = _("Email Types")

    def __str__(self):
        return self.name

    def get_rendered_content(self, context):
        template_content = ''
        with self.template.open('r') as file:
            template_content = file.read()
        template = Template(template_content)
        rendered_content = template.render(Context(context, autoescape=False))
        return rendered_content


class CampaignEmail(models.Model):
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
    body = RichTextField(
        blank=False, null=False, verbose_name=_("Email Body")
    )
    # is_active = models.BooleanField(verbose_name=_("Published"), default=False)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Create"))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("Date Modified"))

    class Meta:
        verbose_name = _("CampaignEmail")
        verbose_name_plural = _("CampaignEmails")

    def __str__(self):
        return self.campaign.__str__()


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
        upload_to=generate_filename,
        verbose_name=_("File"),
        help_text=_("format: Only .mp3, .m4a and .wav files are allowed."),
        validators=[
            validate_file_extension,
            validate_file_size,
            validate_file_duration,
        ],
        blank=True,
        null=True,
    )
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Create"))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("Date Modified"))

    class Meta:
        verbose_name = _("CampaignAudio")
        verbose_name_plural = _("CampaignAudios")

    def __str__(self):
        return self.campaign.__str__()


def logo_image(instance, filename):
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    extension = filename.split('.')[-1]
    return f'images/website/{timestamp}.{extension}'


class Settings(models.Model):
    site_name = models.CharField(
        max_length=255, null=False, blank=False, verbose_name=_("Site Name"),
        help_text=_("format:max-255, the name of website")
    )
    tax = models.IntegerField(
        default=0, verbose_name=_("Tax"),
        help_text=_(
            "format: enter as percentage , it will be use on checkout and use total price for calculation"
        )
    )
    show_result = models.PositiveIntegerField(
        default=3,
        blank=False,
        null=False,
        verbose_name=_("Show Result"),
        help_text=_("format: default-3, days difference between campaign create date and the day they can see result")
    )
    audio_text_length = models.PositiveIntegerField(
        default=400,
        blank=False,
        null=False,
        verbose_name=_("Text to Audio Max Length"),
        help_text=_("format: default-400")
    )
    audio_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        unique=False,
        null=False,
        default=0,
        blank=False,
        verbose_name=_("Audio Price"),
        help_text=_("format: maximum price 99999999.99, used for text to audio extra price"),
        validators=[MinValueValidator(Decimal("0.00"))]
    )
    logo = models.ImageField(
        upload_to=logo_image,
        blank=True,
        null=True,
        verbose_name=_("Main Logo"),
        help_text=_("format: JPEG,JPG,PNG,SVG,WEBP")
    )
    dashboard_logo = models.ImageField(
        upload_to=logo_image,
        blank=True,
        null=True,
        verbose_name=_("Dashboard Logo"),
        help_text=_("format: JPEG,JPG,PNG,SVG,WEBP")
    )
