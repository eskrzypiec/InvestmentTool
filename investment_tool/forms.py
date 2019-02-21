from django import forms
from django.forms import fields

from .models import *

FREQUENCY_CHOICES = [
    (0, 'monthly'),
]


class CreateInvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        exclude = ['created_by', 'approved', 'approver']


class ApproverMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class ApproverForm(forms.Form):
    approver = ApproverMultipleChoiceField(queryset=User.objects.all(), widget=forms.SelectMultiple,
                                           label="Osoba akceptująca")


class AddBenefitForm(forms.ModelForm):
    start_date = fields.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    end_date = fields.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    frequency = fields.ChoiceField(choices=FREQUENCY_CHOICES)

    class Meta:
        model = Benefit
        fields = ['name', 'frequency', 'start_date', 'end_date', 'amount']
        widgets = {'investment': forms.HiddenInput()}


class AddOperatingCostForm(forms.ModelForm):
    start_date = fields.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    end_date = fields.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    frequency = fields.ChoiceField(choices=FREQUENCY_CHOICES)

    class Meta:
        model = OperatingCost
        fields = ['name', 'frequency', 'start_date', 'end_date', 'amount']
        widgets = {'investment': forms.HiddenInput()}


class SearchForm(forms.Form):
    name = forms.CharField(label='', max_length=200, required=False,
                           widget=forms.TextInput(
                               attrs={'placeholder': 'Szukaj projektu', 'class': 'placeholder'}))


class AddAssetForm(forms.ModelForm):
    date = fields.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Asset
        fields = ['name', 'date', 'amount', 'depreciation_period']
        widgets = {'investment': forms.HiddenInput()}


class AddImplementationCostForm(forms.ModelForm):
    date = fields.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = ImplementationCost
        fields = ['name', 'date', 'amount']
        widgets = {'investment': forms.HiddenInput()}
