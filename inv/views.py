from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.forms.formsets import formset_factory, BaseFormSet

from .forms import PartForm, TransactionForm
from .models import Transaction, Part


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    context = {'title': 'Inventory'}

    return render(request,
                  'inv/index.html',
                  context)


def new_transaction(request):
    # Create the formset, specifying the form and formset we want to use.
    PartFormSet = formset_factory(PartForm, formset=BaseFormSet)

    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        part_formset = PartFormSet(request.POST)

        if transaction_form.is_valid() and part_formset.is_valid():
            transaction = transaction_form.save()
            # Now save the data for each form in the formset
            new_parts = []

            for part_form in part_formset:
                name = part_form.cleaned_data.get('name')
                part_number = part_form.cleaned_data.get('part_number')
                location = part_form.cleaned_data.get('location')

                if name and part_number:
                    new_parts.append(Part(transaction=transaction, name=name,
                                          part_number=part_number, location=location))

            Part.objects.bulk_create(new_parts)
            return HttpResponseRedirect(reverse('inv:home'))
    else:
        transaction_form = TransactionForm()
        part_formset = PartFormSet()

    context = {
        'title': 'New Transaction',
        'transaction_form': transaction_form,
        'part_formset': part_formset,
    }

    return render(request, 'inv/transaction_form.html', context)
