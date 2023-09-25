from django import forms
from .models import Campaign, CampaignType, CampaignZip, CampaignSMS, CampaignSMSType, CampaignEmailType, CampaignEmail, \
    CampaignAudio
from django.utils.translation import gettext_lazy as _
from .validators import validate_file_duration


class CampaignAudioForm(forms.ModelForm):
    file = forms.FileField(
        required=True,
        label=_("Select & Upload File"),
        help_text=_("File format will be .mp3/.m4a/.wav, max size 20MB, max duration 45 second"),
        widget=forms.ClearableFileInput(
            attrs={
                "class": "custom-file-input mx-auto",
                "name": "campaignAudio-file",
                "id": "campaignAudio-file"
            }
        )
    )

    class Meta:
        model = CampaignAudio
        fields = ["file"]


class CampaignEmailForm(forms.ModelForm):
    type = forms.ModelChoiceField(
        required=True,
        label=_("Salutation Type"),
        queryset=CampaignEmailType.objects.filter(is_active=True),
        empty_label=None,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "name": "campaignEmail-type",
                "id": "campaignEmail-type"
            }
        )
    )
    subject = forms.CharField(
        max_length=255, required=True, label=_("Email Subject"), widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "name": "campaignEmail-subject",
                "id": "campaignEmail-subject",
            }
        )
    )
    body = forms.CharField(
        required=True, label=_("Email Body"), widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "name": "campaignEmail-body",
                "id": "campaignEmail-body",
            }
        )
    )

    class Meta:
        model = CampaignEmail
        fields = ["type", "subject", "body"]


class CampaignSMSForm(forms.ModelForm):
    type = forms.ModelChoiceField(
        required=True,
        label=_("Salutation Type"),
        queryset=CampaignSMSType.objects.filter(is_active=True),
        empty_label=None,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "name": "campaignSMS-type",
                "id": "campaignSMS-type"
            }
        )
    )
    body = forms.CharField(
        required=True, label=_("SMS Body"), widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "name": "campaignSMS-body",
                "id": "campaignSMS-body",
            }
        )
    )

    class Meta:
        model = CampaignSMS
        fields = ["type", "body"]


class CampaignForm(forms.ModelForm):
    type = forms.ModelChoiceField(
        required=True,
        label=_("Campaign Type"),
        queryset=CampaignType.objects.filter(is_active=True),
        empty_label=None,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "name": "campaign-type",
                "id": "campaign-type"
            }
        )
    )

    class Meta:
        model = Campaign
        fields = ["type", ]