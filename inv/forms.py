from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import StrictButton

from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['user']


class TransactionSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=True)

    def __init__(self, *args, **kwargs):
        super(TransactionSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_class = 'form-inline pull-right'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.layout = Layout(
            'search',
            StrictButton('Search', css_class='btn-default', type='submit'),
        )


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
