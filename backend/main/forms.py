from django import forms
from .models import Page, ComponentsOnPage, Components


class ComponentsOnPageForm(forms.ModelForm):
    class Meta:
        model = ComponentsOnPage
        fields = '__all__'


class PageAdminForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = '__all__'
