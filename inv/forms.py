from django.forms import ModelForm

from .models import Transaction, Part


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['users']


class PartForm(ModelForm):
    class Meta:
        model = Part
        fields = ['name', 'part_number', 'location']
