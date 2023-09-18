from django import forms
from .models import Campaign, CampaignType, CampaignZip
from django.utils.translation import gettext_lazy as _


class CampaignForm(forms.ModelForm):
    type = forms.ModelChoiceField(
        required=True,
        label=_("Campaign Type"),
        queryset=CampaignType.objects.filter(is_active=True),
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "name": "campaign-type",
                "id": "campaign-type"
            }
        )
    )

    total = forms.IntegerField(
        min_value=1, label=_("Total Households"), required=True, initial=1, widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "name": "campaign-total",
                "id": "campaign-total"
            }
        )
    )
    class Meta:
        model = Campaign
        fields = ["type", "total", "zips"]
