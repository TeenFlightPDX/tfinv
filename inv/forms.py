from django import forms
from django.forms import ModelForm

from .models import Transaction, Part


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['users']


class PartForm(forms.Form):
    name = forms.CharField(max_length=75, required=True)
    part_number = forms.CharField(max_length=20, required=True)
    location = forms.CharField(max_length=20, required=False)
