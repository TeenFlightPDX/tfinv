from django import forms

from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['users']


class PartChangeForm(forms.Form):
    name = forms.CharField(max_length=75, required=True)
    part_number = forms.CharField(max_length=20, required=True)
    quantity = forms.IntegerField(required=True)
    location = forms.CharField(max_length=20, required=False)


class PartChangeFormSet(forms.BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(PartChangeFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False
