import os.path
import os

from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator, FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django_ckeditor_5.fields import CKEditor5Field
from django.urls import reverse
from autoslug import AutoSlugField
from mptt.models import TreeForeignKey, MPTTModel

from campaign.validators import video_validator, ticket_safe_extensions
from core.models import BaseModel, UploadPath


class Categories(MPTTModel, BaseModel):
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
    parent = TreeForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="children",
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Parent"),
        help_text=_("format : not required")
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:category', args=[str(self.slug)])


class Components(BaseModel):
    user = models.ForeignKey(
        get_user_model(),
        verbose_name=_("Author"),
        related_name="component_author",
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        help_text=_("format: required")
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        blank=False,
        null=False,
        unique=False,
        help_text=_("format: required, max-255 character, name of your component")
    )
    slug = AutoSlugField(
        allow_unicode=True,
        populate_from="name",
        editable=True,
        unique=True,
        verbose_name=_("Safe URL"),
        blank=True,
        null=False,
    )
    template = models.FileField(
        upload_to=UploadPath("components", "template"),
        blank=False,
        null=False,
        validators=[FileExtensionValidator(allowed_extensions=["html", "htm"])],
        verbose_name=_("Template"),
        help_text=_("format: only .html .htm are allowed"),
    )
    is_public = models.BooleanField(verbose_name=_("Public Component"), default=False)

    class Meta:
        ordering = ["-id"]
        verbose_name = _("Component")
        verbose_name_plural = _("Components")

    def __str__(self):
        return f"{self.user.username} : {self.name}"


class Page(models.Model):
    class TypeChoices(models.TextChoices):
        SIGNIN = "signIn", _("Signin Page")
        SIGNUP = "signUp", _("Signup Page")
        HOME = "home", _("Home Page")
        ABOUT = "about", _("About Page")
        CONTACT = "contact", _("ContactUS Page")
        CATEGORY = "category", _("Category Pages")
        PRIVACY = "privacy", _("Privacy Page")
        TERMS = "terms", _("Terms Page")
        REFUND = "refund", _("Refund Page")
        FEEDBACK = "feedback", _("Feedback Page")

    category = models.OneToOneField(
        Categories,
        verbose_name=_("Category"),
        related_name="category_page",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text=_(
            "format: enter value only if you are creating record for category otherwise leave it empty"
        )
    )
    type = models.CharField(
        max_length=255,
        choices=TypeChoices.choices,
        blank=False,
        null=False,
        default=TypeChoices.CATEGORY,
        help_text=_(
            "format: create only 1 record with types , example only create 1 home page record rest wont be count except category"
        )
    )
    background_text = CKEditor5Field(
        blank=True, null=True, verbose_name=_("Background Text"), config_name="admin",
    )
    background = models.ImageField(
        upload_to=UploadPath('pages', 'background'),
        blank=True,
        null=True,
        verbose_name=_("Background Image"),
        help_text=_("format: JPEG,JPG,PNG,SVG,WEBP")
    )
    body = CKEditor5Field(
        blank=True, null=True, verbose_name=_("Body"), config_name="admin",
    )
    components = models.ManyToManyField(
        Components,
        through='ComponentsOnPage',
        verbose_name=_("Components"),
        help_text=_("format: select components you want to show on the page"),

    )

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")

    def __str__(self):
        if self.category:
            return self.category.name
        else:
            return self.type


class ComponentsOnPage(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    component = models.ForeignKey(Components, on_delete=models.CASCADE)
    index = models.PositiveSmallIntegerField(
        default=1,
        verbose_name=_("Index Ordering"),
        help_text=_("format: order rendering on page")
    )

    class Meta:
        unique_together = ("page", "component")
        ordering = ["-index"]


class Seo(models.Model):
    page = models.OneToOneField(
        Page, related_name="page_seo", blank=False, null=False,
        verbose_name=_("Belonging Page"), on_delete=models.CASCADE
    )
    seo_title = models.CharField(
        max_length=255, blank=False, null=False, verbose_name=_("Seo Title"),
        help_text=_("For SEO purposes, ideally between 60-70 characters.")
    )
    seo_description = models.TextField(
        max_length=160, blank=False, null=False, verbose_name=_("Seo Description"),
        help_text=_("For SEO purposes, ideally between 150-160 characters.")
    )
    seo_canonical = models.URLField(blank=False, null=False, verbose_name=_("Seo Canonical"))
    seo_keywords = models.TextField(
        blank=False, null=False, verbose_name=_("Seo Keywords"),
        help_text=_("Comma-separated list of keywords.")
    )
    seo_is_robots_index = models.BooleanField(
        default=False, verbose_name=_("Seo Robot Index"),
        help_text=_("Set to allow search engines to index this page.")
    )
    seo_is_robots_follow = models.BooleanField(
        default=False, verbose_name=_("Seo Robot Follow"),
        help_text=_("Set to allow search engines to follow links on this page.")
    )
    json_ld_data = models.TextField(
        blank=True, null=True, verbose_name="JSON-LD Data",
        help_text="Enter JSON-LD data for structured information (if applicable)."
    )

    class Meta:
        verbose_name = _("SEO")
        verbose_name_plural = _("SEO")

    def __str__(self):
        return str(self.id)


class FAQ(BaseModel):
    question = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name=_("Question"),
        help_text=_("format: max-255 , required")
    )
    answer = models.TextField(
        verbose_name=_("Answer"),
        blank=False, null=False,
        help_text=_("format: required")
    )

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQ")
        ordering = ["-id"]

    def __str__(self):
        return self.question


class CustomerVideo(BaseModel):
    video = models.FileField(
        upload_to=UploadPath("video", "customer"),
        blank=True,
        null=True,
        verbose_name=_("Video"),
        help_text=_("format: Only .webm , .mov , .ogg , .mp4 and .mkv files are allowed."),
        validators=[
            video_validator
        ],
    )
    thumbnail = models.ImageField(
        upload_to=UploadPath("images", "website"),
        blank=True,
        null=True,
        verbose_name=_("Introduction Thumbnail"),
        help_text=_("format: JPEG,JPG,PNG,SVG,WEBP")
    )

    class Meta:
        ordering = ["-id"]

    def get_video_ext(self):
        try:
            ext = os.path.splitext(self.video.path)[1]
            return ext.split(".")[1]
        except Exception as e:
            print(e)
            return False


class TicketCategory(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        blank=False,
        null=False,
        unique=False,
        help_text=_("format: required, max-255 character, name of your ticket category")
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
        verbose_name = _("Ticket Category")
        verbose_name_plural = _("Ticket Categories")

    def __str__(self):
        return self.name


class Ticket(BaseModel):
    class StatusChoices(models.TextChoices):
        OPEN = "open", _("Open")
        INPROGRESS = "inProgress", _("In Progress")
        RESOLVED = "resolved", _("Resolved")
        CLOSED = "closed", _("Closed")

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='ticket_author',
        verbose_name=_("Author")
    )
    status = models.CharField(
        max_length=20,
        verbose_name=_("Status"),
        choices=StatusChoices.choices,
        default=StatusChoices.OPEN,
    )

    subject = models.CharField(
        max_length=200,
        verbose_name=_("Subject"),
        blank=False,
        null=False,
        help_text=_("format: required , max-200")
    )

    description = models.TextField(
        max_length=3000,
        verbose_name=_("Description"),
        help_text=_("format:required , max-3000"),
        blank=False,
        null=False
    )
    category = models.ForeignKey(
        TicketCategory,
        related_name="ticket_category",
        on_delete=models.SET_NULL,
        verbose_name=_("Category"),
        blank=True,
        null=True,
    )
    is_active = None

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")
        ordering = ["-id"]

    def __str__(self):
        return f"{self.author.username} : {self.subject}"

    def get_last_comment(self):
        queryset = self.ticket_comment.last()
        if queryset and not queryset.author == self.author:
            return True
        else:
            return False

    def get_attachment(self):
        queryset = self.ticket_attachment.filter(ticket_id=self.id, comment__isnull=True)
        return queryset


class TicketComment(BaseModel):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='ticket_comment',
        verbose_name=_("Ticket")
    )
    author = models.ForeignKey(
        get_user_model(),
        verbose_name=_("ticket_comment_author"),
        on_delete=models.CASCADE
    )
    comment = models.TextField(
        max_length=3000,
        verbose_name=_("Comment"),
        help_text=_("format:required , max-3000"),
        blank=False,
        null=False
    )
    is_active = None

    def __str__(self):
        return f'Comment by {self.author.username} on {self.ticket.subject}'

    def get_attachment(self):
        queryset = self.ticket_comment_attachment.filter(
            ticket_id=self.ticket.id,
            comment_id=self.id
        )
        return queryset


class TicketAttachment(BaseModel):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='ticket_attachment')
    comment = models.ForeignKey(
        TicketComment,
        on_delete=models.CASCADE,
        related_name='ticket_comment_attachment',
        null=True,
        blank=True
    )
    file = models.FileField(
        upload_to=UploadPath("tickets", "attachments"),
        blank=False,
        null=False,
        validators=[
            ticket_safe_extensions
        ]
    )
    is_active = None

    def __str__(self):
        return f"Attachment for : {self.ticket.subject}"


class ContactUs(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"), blank=False, null=False)
    email = models.EmailField(verbose_name=_("Email"), blank=False, null=False)
    message = models.TextField(
        max_length=350,
        verbose_name=_("Message"),
        help_text=_("format:required , max-350"),
        blank=False,
        null=False
    )
    is_check = models.BooleanField(verbose_name=_("Is Check"), default=False)
    is_active = None

    class Meta:
        verbose_name = _("Contact Us")
        verbose_name_plural = _("Contact Us")
        ordering = ["-id"]

    def __str__(self):
        return f"{self.id}-{self.name}"


class Settings(models.Model):
    site_name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name=_("Site Name"),
        help_text=_("format:max-255, the name of website")
    )
    tax = models.IntegerField(
        default=0,
        verbose_name=_("Tax"),
        help_text=_(
            "format: enter as percentage , it will be use on checkout and use total price for calculation"
        )
    )
    show_result = models.PositiveIntegerField(
        default=3,
        blank=False,
        null=False,
        verbose_name=_("Show Result"),
        help_text=_(
            "format: default-3, days difference between campaign create date and the day they can see result"
        )
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
        default=10.00,
        blank=False,
        verbose_name=_("Audio Price"),
        help_text=_(
            "format: default-10.00,  maximum price 99999999.99, used for text to audio extra price"
        ),
        validators=[MinValueValidator(Decimal("0.00"))]
    )
    logo = models.ImageField(
        upload_to=UploadPath("images", "website"),
        blank=True,
        null=True,
        verbose_name=_("Main Logo"),
        help_text=_("format: JPEG,JPG,PNG,SVG,WEBP")
    )
    dashboard_logo = models.ImageField(
        upload_to=UploadPath("images", "website"),
        blank=True,
        null=True,
        verbose_name=_("Dashboard Logo"),
        help_text=_("format: JPEG,JPG,PNG,SVG,WEBP")
    )
    intro_video = models.FileField(
        upload_to=UploadPath("video", "website"),
        blank=True,
        null=True,
        verbose_name=_("Introduction Video"),
        help_text=_("format: Only .webm , .mov , .ogg , .mp4 and .mkv files are allowed."),
        validators=[
            video_validator
        ],
    )
    intro_thumbnail = models.ImageField(
        upload_to=UploadPath("images", "website"),
        blank=True,
        null=True,
        verbose_name=_("Introduction Thumbnail"),
        help_text=_("format: JPEG,JPG,PNG,SVG,WEBP")
    )
    facebook = models.URLField(
        verbose_name=_("Facebook"),
        help_text=_("format: absolute URL"),
        blank=True,
        null=True
    )
    instagram = models.URLField(
        verbose_name=_("Instagram"),
        help_text=_("format: absolute URL"),
        blank=True,
        null=True
    )
    x_twitter = models.URLField(
        verbose_name=_("X(Twitter)"),
        help_text=_("format: absolute URL,"),
        blank=True,
        null=True
    )
    youtube = models.URLField(
        verbose_name=_("Youtube"),
        help_text=_("format: absolute URL"),
        blank=True,
        null=True
    )
    api_token = models.TextField(
        verbose_name=_("Api Token"),
        help_text=_("format: used in post request to create campaign"),
        blank=True,
        null=True, )

    def get_video_ext(self):
        try:
            ext = os.path.splitext(self.intro_video.path)[1]
            return ext.split(".")[1]
        except Exception as e:
            print(e)
            return False
