from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import User
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = "__all__"


class CustomUserChangeForm(UserChangeForm):
    phone_number = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(
            attrs={
                "style": "margin-left:10px"
            }
        ), required=False,
    )

    class Meta:
        model = User
        fields = "__all__"
