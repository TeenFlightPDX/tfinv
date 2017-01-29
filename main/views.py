"""
Definition of views.
"""
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    context = {}

    return render(request,
                  'main/index.html',
                  context)
