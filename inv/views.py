from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
from django.db import IntegrityError, transaction as db_transaction

from crispy_forms.layout import Submit
from django_tables2 import RequestConfig

from .forms import PartChangeForm, PartChangeFormSet, PartChangeFormSetHelper, TransactionSearchForm
from .models import PartChange, Transaction
from .tables import TransactionViewTable, PartChangeTable


def home(request):
    assert isinstance(request, HttpRequest)

    results = Transaction.objects.filter(approved=True)

    # search = ''

    if request.method == 'POST':
        search_form = TransactionSearchForm(request.POST)

        # if search_form.is_valid():
        # search = search_form.cleaned_data['search']
        # TODO: filter the queryset with the search term
    else:
        search_form = TransactionSearchForm()

    table = TransactionViewTable(results, order_by='-time')
    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    context = {'title': 'Inventory', 'table': table, 'search_form': search_form}

    return render(request, 'inv/index.html', context)


def view_transaction(request, id):
    try:
        transaction = Transaction.objects.get(id=id)
        parts = transaction.getParts()
    except (Transaction.DoesNotExist, ValueError):
        # Error - invalid page, return to home
        return HttpResponseRedirect(reverse('inv:home'))

    table = PartChangeTable(parts)
    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    context = {'title': 'Transaction Detail', 'table': table, 'transaction': transaction}

    return render(request, 'inv/view_transaction.html', context)


def edit_transaction(request, id):
    transaction = Transaction.objects.get(id=id)

    # Only the user that made the transaction can edit it
    if not request.user == transaction.user:
        return HttpResponseRedirect(reverse('inv:view_transaction', args=[id]))

    PartInlineFormSet = inlineformset_factory(Transaction, PartChange, fields=('name', 'location', 'part_number'))

    if request.method == "POST":
        formset = PartInlineFormSet(request.POST, request.FILES, instance=transaction)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('inv:view_transaction', args=[id]))
    else:
        formset = PartInlineFormSet(instance=transaction)

    # Helper for formatting inline formset with crispy forms
    helper = PartChangeFormSetHelper()
    helper.template = 'inv/table_inline_formset_js.html'
    helper.form_class = 'part-formset'
    helper.add_input(Submit("submit", "Save"))

    context = {
        'title': 'Edit Transaction',
        'part_formset': formset,
        'helper': helper
    }

    return render(request, 'inv/edit_transaction.html', context)


@login_required
def new_transaction(request):
    # Create the formset, specifying the form and formset we want to use.
    partchangeformset = formset_factory(PartChangeForm, min_num=1, extra=0, formset=PartChangeFormSet)

    if request.method == 'POST':
        part_formset = partchangeformset(request.POST)

        if part_formset.is_valid():
            transaction = Transaction
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
        part_formset = partchangeformset(initial=[{'quantity': 1}])

    # Helper for formatting inline formset with crispy forms
    helper = PartChangeFormSetHelper()
    helper.template = 'inv/table_inline_formset_js.html'
    helper.form_class = 'part-formset'
    helper.add_input(Submit("submit", "Save"))

    context = {
        'title': 'New Transaction',
        'part_formset': part_formset,
        'helper': helper,
    }

    return render(request, 'inv/new_transaction.html', context)
