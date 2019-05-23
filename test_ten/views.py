import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from ten.decorators import tenant_required
from ten.helpers.tenant import get_tenants

from . models import Collaboration, Tenant, ScheduledService, Patient
from . forms import CreateUserForm, TenantForm, PatientForm, ScheduledServiceForm


def home(request):
    print('home')
    print('request: ', request)
    template_name = 'home.html'
    context = {
        'title': 'Home',
        'subtitle': 'Home subtitle',
    }
    
    if request.user.is_authenticated:
        print('authenticated')
        context['tenants'] = get_tenants()

    return render(request, template_name, context)


def account_create(request):
    template_name = 'account_create.html'
    context = {
        'title': 'Account Create',
        'subtitle': '',
    }

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = User()
            user.username = form.cleaned_data['username']
            user.password = form.cleaned_data['password']
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']

            user.set_password(user.password) # https://docs.djangoproject.com/en/2.0/ref/contrib/auth/#django.contrib.auth.models.User.set_password
            user.save()
    else:
        form = CreateUserForm()
    
    context['form'] = form

    return render(request, template_name, context)


@login_required
def tenant_create(request):
    template_name = 'tenant_create.html'
    context = {
        'title': 'Create Tenant',
        'subtitle': 'Create new tenant',
    }

    if request.method == 'POST':
        form = TenantForm(request.POST)

        if form.is_valid():
            form.save()
            Collaboration.objects.create(tenant=form.instance, owner=True)
            return redirect('home')
    else:
        form = TenantForm()
    
    context['form'] = form

    return render(request, template_name, context)


@tenant_required
def patient_create(request):
    template_name ='patient_create.html'
    context = {
        'title': 'Create Patient',
        'subtitle': 'Create new patient',
    }

    if request.method == 'POST':
        form = PatientForm(request.POST)

        if form.is_valid():
            form.save()
            #Patient.objects.create(name='Za')
            #Patient.objects.create(name='Ze', add_current_tenant=False)
        else:
            print('Form is not valid')

    form = PatientForm()
    
    context['form'] = form
    
    return render(request, template_name, context)


@tenant_required
def scheduled_service_create(request):
    template_name ='scheduled_service_create.html'
    context = {
        'title': 'Create Scheduled Service',
        'subtitle': 'Create new scheduled service',
    }

    if request.method == 'POST':
        form = ScheduledServiceForm(request.POST)

        if form.is_valid():
            form.save()


    form = ScheduledServiceForm()
    
    context['form'] = form
    
    return render(request, template_name, context)


@tenant_required
def scheduled_service_list(request):
    template_name ='scheduled_service_list.html'
    context = {
        'title': 'Scheduled Service List',
        'subtitle': 'your schedules services',
    }

    scheduled_services = ScheduledService.objects.all()
    print(scheduled_services)
    context['scheduled_services'] = scheduled_services

    return render(request, template_name, context)


def tenant_active(request, pk):
    tenant = Tenant.objects.get(id=int(pk))
    tenant.activate()

    return redirect('/')
    
