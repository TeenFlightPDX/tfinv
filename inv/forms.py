from django import forms

from crispy_forms.helper import FormHelper

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


class PartChangeFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PartChangeFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'POST'
        self.render_required_fields = True
