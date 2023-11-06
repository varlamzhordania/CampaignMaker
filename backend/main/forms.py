from django import forms
from .models import Page, ComponentsOnPage, Components, Ticket, TicketCategory, TicketAttachment, TicketComment
from django.utils.translation import gettext_lazy as _


class TicketAttachmentForm(forms.ModelForm):
    file = forms.FileField(
        required=False, label=_("Attachment"), widget=forms.FileInput(
            attrs={
                "class": "custom-file-input mx-auto",
                "name": "attachment-1",
                "id": "attachment-1",
            }
        )
    )

    class Meta:
        model = TicketAttachment
        fields = ["file"]


class TicketCommentCreateForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        label='Comment'
    )

    class Meta:
        model = TicketComment
        fields = ["comment"]


class TicketCreateForm(forms.ModelForm):
    subject = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Subject'
    )
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        label='Description'
    )
    category = forms.ModelChoiceField(
        queryset=TicketCategory.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label=None
    )

    class Meta:
        model = Ticket
        fields = ["subject", "description", "category"]


class ComponentsOnPageForm(forms.ModelForm):
    class Meta:
        model = ComponentsOnPage
        fields = '__all__'


class PageAdminForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = '__all__'
