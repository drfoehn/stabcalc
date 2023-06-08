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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from calculator import views
from calculator.views import *
# from calculator.admin import user_dashboard
# from django.contrib.auth import views as auth_views

urlpatterns = [

    path('admin/', admin.site.urls, name='admin'),
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("about/", TemplateView.as_view(template_name="about.html"), name='about'),
    path("terms_condition/", TemplateView.as_view(template_name="terms_conditions.html"), name='terms_conditions'),
    path("calculator/", include('calculator.urls')),
    path("database/", include('database.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),
    path('itemlists/', views.item_lists, name="itemlists"),
    path('unregistered_user/', TemplateView.as_view(template_name="unregistered_user.html"), name='unregistered_user'),
]
