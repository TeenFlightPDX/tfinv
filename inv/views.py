from django.contrib import messages
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.forms.formsets import formset_factory
from django.db import IntegrityError, transaction as db_transaction

from crispy_forms.layout import Submit

from .forms import PartChangeForm, TransactionForm, PartChangeFormSet, PartChangeFormSetHelper
from .models import PartChange


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    context = {'title': 'Inventory'}

    return render(request,
                  'inv/index.html',
                  context)


def new_transaction(request):
    # Create the formset, specifying the form and formset we want to use.
    partchangeformset = formset_factory(PartChangeForm, min_num=1, extra=0, formset=PartChangeFormSet)

    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        part_formset = partchangeformset(request.POST)

        if transaction_form.is_valid() and part_formset.is_valid():
            transaction = transaction_form.save()
            # Now save the data for each form in the formset
            new_parts = []

            for part_form in part_formset:
                name = part_form.cleaned_data.get('name')
                part_number = part_form.cleaned_data.get('part_number')
                location = part_form.cleaned_data.get('location')

                if name and part_number:
                    new_parts.append(PartChange(transaction=transaction, name=name,
                                                part_number=part_number, location=location))

            try:
                with db_transaction.atomic():
                    PartChange.objects.bulk_create(new_parts)
                    messages.success(request, 'You have submitted a transaction.')
                    return HttpResponseRedirect(reverse('inv:home'))

            except IntegrityError:  # If the transaction failed
                messages.error(request, 'There was an error saving your transaction.')
                return HttpResponseRedirect(reverse('inv:new_transaction'))

    else:
        transaction_form = TransactionForm()
        part_formset = partchangeformset()

    # Helper for formatting inline formset with crispy forms
    helper = PartChangeFormSetHelper()
    helper.template = 'inv/table_inline_formset_js.html'
    helper.form_class = 'part-formset'
    helper.add_input(Submit("submit", "Save"))

    context = {
        'title': 'New Transaction',
        'transaction_form': transaction_form,
        'part_formset': part_formset,
        'helper': helper,
    }

    return render(request, 'inv/transaction_form.html', context)
