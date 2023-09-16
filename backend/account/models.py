from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class User(AbstractUser):
    middle_name = models.CharField(max_length=255, verbose_name=_("Middle Name"), blank=True, null=True, unique=False)
    phone_number = PhoneNumberField(blank=True, null=True, verbose_name=_("Phone Number"))
    business_name = models.DateField(verbose_name=_("Business Name"), blank=True, null=True)
    last_ip = models.GenericIPAddressField(verbose_name=_("Last IP Address"), null=True, blank=True)

    def __str__(self):
        return self.username

    def get_full_name(self):
        if not self.middle_name and not self.first_name and not self.last_name:
            return self.username
        return f"{self.first_name} {self.middle_name} {self.last_name}"
