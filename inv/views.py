from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse

from .forms import PartForm, TransactionForm
from .models import Transaction, Part

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    context = {'title': 'Inventory'}

    return render(request,
                  'inv/index.html',
                  context)
