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
from django.urls import path
from django.views.generic import TemplateView

from calculator import views
from calculator.admin import user_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', user_dashboard.urls),
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    # path("dashboard/", TemplateView.as_view(template_name="dashboard.html"), name="dashboard"),
    path("add-instrument/", views.InstrumentAddView.as_view(), name="add_instrument"),
    path("instrument-list", views.InstrumentIndex.as_view(), name="instrument_list"),
    path("instrument/<pk>/edit", views.InstrumentUpdateView.as_view(), name="edit_instrument"),
    path("add-sample/", views.SampleAddView.as_view(), name="add_sample"),
    path("add-parameter/", views.ParameterAddView.as_view(), name="add_parameter"),
    path("instrument-list", views.InstrumentIndex.as_view(), name="instrument_list"),

]
