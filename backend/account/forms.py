from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, \
    PasswordResetForm, SetPasswordForm
from phonenumber_field.formfields import PhoneNumberField,SplitPhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import User
from django import forms
from django.utils.translation import gettext_lazy as _


class StylesCustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control border-always outline-0 shadow-0 lh-lg",
                "name": "new_password1",
                "id": "new_password1",
                "placeholder": "New password",
            }
        ),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control border-always outline-0 shadow-0 lh-lg",
                "name": "new_password2",
                "id": "new_password2",
                "placeholder": "Confirm your new password",
            }
        ),
    )


class StylesCustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control border-always outline-0 shadow-0 lh-lg",
                "name": "email",
                "id": "email",
                "placeholder": "Email",
            }
        ),
    )


class StylesCustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        max_length=128, min_length=8, required=True,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "autofocus": True,
                "class": "form-control border-always outline-0 shadow-0 lh-lg",
                "name": "old_password",
                "id": "old_password",
                "placeholder": "Your old password",
            }
        ),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        max_length=128, min_length=8, required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control border-always outline-0 shadow-0 lh-lg",
                "name": "new_password1",
                "id": "new_password1",
                "placeholder": "New password",
            }
        ),
    )

    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        max_length=128, min_length=8, required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control border-always outline-0 shadow-0 lh-lg",
                "name": "new_password2",
                "id": "new_password2",
                "placeholder": "Confirm your new password",
            }
        ),
    )

    class Meta:
        model = User
        fields = "__all__"


class StylesCustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField(
        max_length=150, required=True, label=_("First Name"), widget=forms.TextInput(
            attrs={
                "class": "form-control border-always outline-0 shadow-0 lh-lg",
                "name": "first_name",
                "id": "first_name",
                "placeholder": "First Name",
            }
        )
    )
    middle_name = forms.CharField(
        max_length=150, required=False, label=_("Middle Name"), widget=forms.TextInput(
            attrs={
                "class": "form-control border-always outline-0 shadow-0 lh-lg",
                "name": "middle_name",
                "id": "middle_name",
                "placeholder": "Middle Name",
            }
        )
    )
    last_name = forms.CharField(
        max_length=150, required=True, label=_("Last Name"), widget=forms.TextInput(
            attrs={
                "class": "form-control border-always outline-0 shadow-0 lh-lg",
                "name": "last_name",
                "id": "last_name",
                "placeholder": "Last Name",
            }
        )
    )

    email = forms.EmailField(
        disabled=True, required=True, label=_("Email"), widget=forms.EmailInput(
            attrs={
                "class": "form-control border-always outline-0 shadow-0 lh-lg",
                "name": "email",
                "id": "email",
                "placeholder": "Email",
            }
        )
    )

    phone_number = PhoneNumberField(
        disabled=True, required=True, label="Phone", widget=forms.TextInput(
            attrs={
                "class": "form-control border-always outline-0 shadow-0 lh-lg",
                "name": "phone_number",
                "id": "phone_number",
                "placeholder": "Phone Number",
            }
        )
    )

    class Meta:
        model = User
        fields = ["email", "phone_number", "first_name", "middle_name", "last_name"]


class StylesCustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150, required=True, label=_("First Name"), widget=forms.TextInput(
            attrs={
                "class": "form-control border-always outline-0 shadow-0 lh-lg",
                "name": "first_name",
                "id": "first_name",
                "placeholder": "First Name",
            }
        )
    )
    middle_name = forms.CharField(
        max_length=150, required=False, label=_("Middle Name"), widget=forms.TextInput(
            attrs={
                "class": "form-control border-always outline-0 shadow-0 lh-lg",
                "name": "middle_name",
                "id": "middle_name",
                "placeholder": "Middle Name",
            }
        )
    )
    last_name = forms.CharField(
        max_length=150, required=True, label=_("Last Name"), widget=forms.TextInput(
            attrs={
                "class": "form-control border-always outline-0 shadow-0 lh-lg",
                "name": "last_name",
                "id": "last_name",
                "placeholder": "Last Name",
            }
        )
    )

    email = forms.EmailField(
        required=True, label=_("Email"), widget=forms.EmailInput(
            attrs={
                "class": "form-control border-always outline-0 shadow-0 lh-lg",
                "name": "email",
                "id": "email",
                "placeholder": "Email",
            }
        )
    )

    username = forms.CharField(
        max_length=150, label=_("Username"), required=True, widget=forms.TextInput(
            attrs={
                "class": "form-control border-always outline-0 shadow-0 lh-lg",
                "name": "username",
                "id": "username",
                "placeholder": "Username",
            }
        )
    )
    password1 = forms.CharField(
        max_length=128, min_length=8, label=_("Password"), required=True, widget=forms.PasswordInput(
            attrs={
                "class": "form-control border-always outline-0 shadow-0 lh-lg",
                "name": "password1",
                "id": "password1",
                "placeholder": "****",
            }
        )
    )
    password2 = forms.CharField(
        max_length=128, min_length=8, label=_("Confirm Password"), required=True, widget=forms.PasswordInput(
            attrs={
                "class": "form-control border-always outline-0 shadow-0 lh-lg",
                "name": "password2",
                "id": "password2",
                "placeholder": "****",
            }
        )
    )

    phone_number = PhoneNumberField(
        required=True, label="Phone", widget=forms.TextInput(
            attrs={
                "class": "form-control border-always outline-0 shadow-0 lh-lg",
                "name": "phone_number",
                "id": "phone_number",
                "placeholder": "+1XXXXXXXXXX",
            }
        )
    )

    class Meta:
        model = User
        fields = ["first_name", "middle_name", "last_name", "username", "email", "phone_number",
                  "password1", "password2", ]


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = "__all__"


class CustomUserChangeForm(UserChangeForm):

    phone_number = SplitPhoneNumberField(required=False,)


    class Meta:
        model = User
        fields = "__all__"
