from django import forms

from .models import Step


class CSVUploadForm(forms.Form):
    file = forms.FileField()
    auto_confirm = forms.BooleanField(initial=True, required=False)


class StepStatusForm(forms.Form):
    status = forms.ChoiceField(choices=Step.STATUS_CHOICES, label="", initial='', widget=forms.Select(), required=True)
    new_note = forms.CharField(required=False, strip=True)
