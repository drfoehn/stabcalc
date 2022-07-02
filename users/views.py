from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.template.loader import get_template
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.urls import reverse_lazy

from .forms import *
from django.utils.translation import gettext_lazy as _
from calculator.models import *

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
            username = form.cleaned_data['user_name']
            email = form.cleaned_data['email']
            # password1 = form.cleaned_data['password1']
            # LabUser = authenticate(username=username, password=password1)
            # login(request, LabUser)
            #############Create and send authentication e-mail#####################
            htmly = get_template('users/email.html')
            d = {'username': username }
            subject, from_email, to = 'welcome', 'administrator@eflm.eu', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            ########################################
            messages.success(request, _('Registration successful! Your application will be reviewed by the administrator. You will get a notification as soon as your account has been activated.'))
            return redirect('index')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register_user.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['login_email']
        password = request.POST['login_password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f' Welcome {username} !!')
            return redirect('index')
        else:
            messages.success(request, _('There was an error. Please try again or contact the administrator'))
            return redirect('login')
    form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

        # class UserUpdateView(view.UpdateView):
        #     user=User.objects.get(pk=pk)
        #     pass
        # return render(request, 'users/my-profile.html', {})

@login_required
def user_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f' Your profile was updated successfully.')
            return redirect('user_profile')
    else:
        form=CustomUserChangeForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})


# class UserUpdateView(view.UpdateView):
#     user=User.objects.get(pk=pk)
#     pass
    # return render(request, 'users/my-profile.html', {})

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name='users/change_password.html'
    messages.success(request, f'Your Password was changed successfully' )
    success_url = reverse_lazy('user_profile')


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




