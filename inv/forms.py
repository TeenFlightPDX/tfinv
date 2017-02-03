from django import forms
from django.forms import ModelForm, BaseFormSet

from .models import Transaction


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['users']


class PartForm(forms.Form):
    name = forms.CharField(max_length=75, required=True)
    part_number = forms.CharField(max_length=20, required=True)
    location = forms.CharField(max_length=20, required=False)


class PartFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(PartFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False
