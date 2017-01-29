"""
Plans Views
"""
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse

from .models import Kit, Section, Page, Step, Step_Note
from .forms import CSVUploadForm, StepStatusForm

from .csvmanager import *


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    context = {'title': 'Plans'}

    kits = Kit.objects.filter().order_by('name')
    context['kits'] = kits

    return render(request,
                  'plans/index.html',
                  context)


def section(request, section_number):
    context = {}
    template = 'plans/section.html'

    try:
        section = Section.objects.get(section_number=section_number)
        pages = section.getConfirmedPages()
    except (Section.DoesNotExist, ValueError):
        # Error - invalid page, return to list of sections
        return HttpResponseRedirect(reverse('home'))
    else:
        context['section'] = section
        context['pages'] = pages
        context['title'] = 'Section ' + section_number

    return render(request, template, context)


def step(request, section_number, page_number, step_number):
    context = {}
    template = 'plans/step.html'

    try:
        section = Section.objects.get(section_number=section_number)
        page = Page.objects.get(section=section, page_number=page_number)
        step = Step.objects.get(page=page, step_number=step_number)
    except (Step.DoesNotExist, ValueError):
        # Error - invalid page, return to list of sections
        return HttpResponseRedirect(reverse('plans:home'))
    else:
        context['section'] = section
        context['page'] = page
        context['step'] = step
        context['title'] = 'Step %s-%s-%s' % (section_number, page_number, step_number)

    return render(request, template, context)


def upload(request):
    context = {'title': 'Plans Upload'}
    template = 'plans/upload.html'

    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            auto_confirm = form.cleaned_data['auto_confirm']
            csvmanager.process_uploaded_csv(
                request.FILES['file'], auto_confirm)

            if auto_confirm:
                return HttpResponseRedirect(reverse('plans:home'))
            else:
                return HttpResponseRedirect(reverse('plans:confirm'))
    else:
        form = CSVUploadForm()

    context['form'] = form
    return render(request, template, context)


def confirm(request):
    context = {'title': 'Plans Confirm'}
    template = 'plans/confirm.html'

    sections = Section.objects.filter(confirmed=False)
    context['sections'] = sections

    return render(request, template, context)


def progress(request):
    context = {'title': 'Plans Progress'}
    template = 'plans/progress.html'

    return render(request, template, context)


def update(request, section_number, page_number, step_number):
    context = {'title': 'Step Update'}
    template = 'plans/step_update.html'

    try:
        section = Section.objects.get(section_number=section_number)
        page = Page.objects.get(section=section, page_number=page_number)
        step = Step.objects.get(page=page, step_number=step_number)
    except (Step.DoesNotExist, ValueError):
        # Error - invalid page, return to list of sections
        return HttpResponseRedirect(reverse('plans:home'))
    else:
        context['section'] = section
        context['page'] = page
        context['step'] = step

        if request.method == 'POST':
            form = StepStatusForm(request.POST)
            if form.is_valid():
                status = form.cleaned_data['status']
                step.status = status
                step.save()

                new_note = form.cleaned_data['new_note']

                if new_note:
                    step_note = Step_Note(step=step, user=request.user, text=new_note)
                    step_note.save()

                return HttpResponseRedirect(reverse('plans:step',
                       kwargs={'section_number': section_number, 'page_number': page_number, 'step_number': step_number}))
        else:
            form = StepStatusForm(initial={'status': step.status})

        context['form'] = form

    return render(request, template, context)
