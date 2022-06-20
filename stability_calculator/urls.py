"""stability_calculator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from calculator import views
from calculator.views import *
from calculator.admin import user_dashboard
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('admin/', admin.site.urls),
    #URLs for Password reset
    #TODO: set up an email backend for the reset link to actually work.
    path('admin/password_reset/',auth_views.PasswordResetView.as_view(),name='admin_password_reset',),
    path('admin/password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done',),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm',),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete',),


    path('dashboard/', user_dashboard.urls),
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    # path("dashboard/", TemplateView.as_view(template_name="dashboard.html"), name="dashboard"),
    path("add-instrument/", views.InstrumentAddView.as_view(), name="add_instrument"),
    path("instrument-list", views.InstrumentIndex.as_view(), name="instrument_list"),
    path("instrument/<pk>/edit", views.InstrumentUpdateView.as_view(), name="edit_instrument"),
    path("add-sample/", views.SampleAddView.as_view(), name="add_sample"),
    path("add-parameter/", views.ParameterAddView.as_view(), name="add_parameter"),
    path("instrument-list", views.InstrumentIndex.as_view(), name="instrument_list"),
    path("add-results/", views.ValuesAddView.as_view(), name="add_results"),
    path("input/", views.MultiInputView.as_view(), name="input"),
    path("results/<pk>", views.ResultsView.as_view(), name="results"),
    path("upload/", views.upload_view, name="upload"),

]
