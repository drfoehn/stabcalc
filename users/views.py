from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from django.utils.translation import gettext_lazy as _
from calculator.models import *

def login_user(request):
    if request.method == 'POST':
        username = request.POST['login_email']
        password = request.POST['login_password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.success(request, _('There was an error. Please try again or contact the administrator'))
            return redirect('login')
    else:
        return render(request, 'users/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, _('You were successfully logged out'))
    return redirect('index')


def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # FIXME: Login after registration throws error: 'AnonymousUser' object has no attribute '_meta'
            # username = form.cleaned_data['user_name']
            # password1 = form.cleaned_data['password1']
            # LabUser = authenticate(username=username, password=password1)
            # login(request, LabUser)
            messages.success(request, _('Registration successful!'))
            return redirect('index')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register_user.html', {'form': form})


def user_dashboard(request):
    settings = Setting.objects.all()
    parameters= Parameter.objects.all()
    subjects= Subject.objects.all()
    durations= Duration.objects.all()
    samples= Sample.objects.all()
    conditions= Condition.objects.all()
    instruments= Instrument.objects.all()

    context = {
        'settings': settings,
        'parameters': parameters,
        'subjects': subjects,
        'durations': durations,
        'samples': samples,
        'conditions': conditions,
        'instruments': instruments,
    }

    return render(request, 'users/dashboard.html', context)




