from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from core.models import BaseModel


class User(AbstractUser):
    email = models.EmailField(_("email address"), blank=True, unique=True)
    middle_name = models.CharField(
        max_length=255,
        verbose_name=_("Middle Name"),
        blank=True,
        null=True,
        unique=False
    )
    phone_number = PhoneNumberField(blank=True, null=True, verbose_name=_("Phone Number"))
    show_questions = models.BooleanField(
        verbose_name=_("Show Questions"),
        default=True,
        help_text=_("Show Questions regard of business")
    )
    last_ip = models.GenericIPAddressField(verbose_name=_("Last IP Address"), null=True, blank=True)

    def __str__(self):
        return self.username

    def get_full_name(self):
        name_parts = [self.first_name, self.middle_name, self.last_name]

        name_parts = [name for name in name_parts if name]

        if not name_parts:
            return self.username

        return " ".join(name_parts)

    def completed_questions(self):
        self.show_questions = False
        self.save(update_fields=["show_questions"])


class Industry(BaseModel):
    name = models.CharField(
        verbose_name=_("Industry Name"),
        max_length=255,
        help_text=_("Enter the name of the industry (e.g., Food & Beverage, Retail, etc.)"),
        blank=False,
        null=False,
    )
    is_active = models.BooleanField(
        verbose_name=_("Published"),
        default=False,
        help_text=_("Indicates if the industry is currently active and visible in the system.")
    )

    class Meta:
        verbose_name = _("Industry")
        verbose_name_plural = _("Industries")

    def __str__(self):
        return self.name


class UserBusinessProfile(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="business_profile",
        help_text=_("The user who owns this business profile.")
    )
    business_name = models.CharField(
        max_length=255,
        verbose_name=_("Business Name"),
        blank=True,
        null=True,
        help_text=_("The name of the business (e.g., 'Coffee Shop' or 'Tech Solutions').")
    )
    industry = models.ForeignKey(
        Industry,
        verbose_name=_("Industry"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Select the industry that best represents the business.")
    )
    location = models.CharField(
        max_length=255,
        verbose_name=_("Business Location"),
        blank=True,
        null=True,
        help_text=_("Enter the physical address or city of your business.")
    )
    website = models.URLField(
        verbose_name=_("Website"),
        blank=True,
        null=True,
        help_text=_("Provide a URL to your business website if available.")
    )
    work_hours = models.CharField(
        max_length=255,
        verbose_name=_("Work Hours"),
        blank=True,
        null=True,
        help_text=_("Enter your business' operating hours (e.g., '9 AM - 5 PM, Mon-Fri').")
    )
    brand_tone = models.CharField(
        max_length=255,
        verbose_name=_("Brand Voice Style"),
        blank=True,
        null=True,
        help_text=_(
            "Describe your business' brand tone (e.g., casual, professional, friendly, etc.)."
        )
    )
    brand_keywords = models.TextField(
        verbose_name=_("Brand Keywords"),
        blank=True,
        null=True,
        help_text=_(
            "List keywords or phrases that best represent your business (e.g., fresh, local, innovative)."
        )
    )

    class Meta:
        verbose_name = _("User Business Profile")
        verbose_name_plural = _("User Business Profiles")

    def __str__(self):
        return f"{self.user.username}'s Business Profile"

    def percentage_done(self):
        fields = [
            self.business_name,
            self.industry,
            self.location,
            self.website,
            self.work_hours,
            self.brand_tone,
            self.brand_keywords,
        ]
        total_fields = len(fields)
        filled_fields = sum([1 for field in fields if field])
        return (filled_fields / total_fields) * 100 if total_fields else 0

    def remaining_fields(self):
        fields = [
            ("Business Name", self.business_name),
            ("Industry", self.industry),
            ("Location", self.location),
            ("Website", self.website),
            ("Work Hours", self.work_hours),
            ("Brand Tone", self.brand_tone),
            ("Brand Keywords", self.brand_keywords),
        ]
        remaining = [field[0] for field in fields if not field[1]]
        return remaining

    def is_profile_complete(self):
        return self.percentage_done() == 100

    def get_incomplete_steps(self):
        return self.remaining_fields()

    def get_profile_progress(self):
        return {
            "percentage": self.percentage_done(),
            "completed": self.is_profile_complete(),
            "remaining_steps": self.get_incomplete_steps(),
        }


class BusinessAudience(BaseModel):
    class GenderChoice(models.TextChoices):
        MALE = "Male", _("Male")
        FEMALE = "Female", _("Female")
        ALL = "all", _("All Genders")

    class AgeRangeChoices(models.TextChoices):
        child = "1-6", _("1-6 years old")
        adolescent = "7-12", _("7-12 years old")
        teenager = "13-19", _("13-19 years old")
        adult = "20-60", _("20-60 years old")
        senior = "60+", _("60+ years old")

    business = models.OneToOneField(
        UserBusinessProfile,
        on_delete=models.CASCADE,
        verbose_name=_("Business Profile"),
        related_name="business_audience",
        blank=True,
        null=True,
    )
    gender = models.CharField(
        max_length=10,
        verbose_name=_("Gender"),
        choices=GenderChoice.choices,
        default=GenderChoice.ALL,
        help_text=_("Select the gender of your audience.")
    )
    age_range = models.CharField(
        max_length=255,
        choices=AgeRangeChoices.choices,
        verbose_name=_("Age Range"),
        help_text=_("Choose the age range of your business' primary audience.")
    )
    interests = models.TextField(
        verbose_name=_("Audience Interests"),
        blank=True,
        null=True,
        help_text=_(
            "Provide details about your target audience's interests (e.g., technology, fashion, food)."
        )
    )
    focus = models.TextField(
        verbose_name=_("Audience Focus"),
        blank=True,
        null=True,
        help_text=_(
            "Describe your audience focus. It could be location-based, interest-based, or based on other criteria."
        )
    )
    is_active = None


class IndustryQuestion(BaseModel):
    class AnswerType(models.TextChoices):
        # CHECKBOX = "checkbox", _("Checkbox")
        # RADIO = "radio", _("Radio")
        TEXT = "text", _("Text")

    industry = models.ForeignKey(
        Industry,
        verbose_name=_("Industry"),
        on_delete=models.CASCADE,
        related_name="questions",
        help_text=_("The industry this question is related to.")
    )
    name = models.CharField(
        verbose_name=_("Question Name"),
        max_length=255,
        help_text=_("The name or description of the question.")
    )
    answer_type = models.CharField(
        verbose_name=_("Answer Type"),
        max_length=12,
        choices=AnswerType.choices,
        default=AnswerType.TEXT,
        help_text=_(
            "Select the type of answer that the question expects (e.g., text, checkbox, or radio)."
        )
    )
    optional = models.BooleanField(
        verbose_name=_("Optional Question"),
        default=False,
        help_text=_(
            "Check if the question is optional. Optional questions can be skipped by users."
        )
    )
    is_active = models.BooleanField(
        verbose_name=_("Published"),
        default=False,
        help_text=_("Indicates if the question is active and visible to users.")
    )
    question_order = models.IntegerField(
        default=0,
        verbose_name=_("Question Order"),
        help_text=_("The order in which this question will appear relative to other questions.")
    )

    class Meta:
        verbose_name = _("Industry Question")
        verbose_name_plural = _("Industry Questions")
        ordering = ['question_order']

    def __str__(self):
        return self.name


class UserIndustryAnswer(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="industry_answers",
        help_text=_("The user who provided this answer.")
    )
    question = models.ForeignKey(
        IndustryQuestion, on_delete=models.CASCADE, related_name="answers",
        help_text=_("The question that was answered by the user.")
    )
    answer = models.JSONField(
        verbose_name=_("Answers"),
        blank=True,
        null=True,
        help_text=_(
            "Answers are stored as a json for better access (e.g., {question:answer}) for checkbox, radio question."
        )
    )
    answered = models.BooleanField(
        default=False,
        verbose_name=_("Answered"),
        help_text=_("Indicates whether the user has answered this question or not.")
    )
    is_active = None

    def __str__(self):
        return f"Answer by {self.user.username} to {self.question.name}"
