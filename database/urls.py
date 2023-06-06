from django.contrib import admin
from django.urls import path, include
from database import views
from database.views import *
# from calculator.admin import user_dashboard
# from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


urlpatterns = [
    path("", views.AnalyteIndex.as_view(), name="analyte_list"),
    # path("add/", views.HikeAddView.as_view(), name="add"),
    path("<int:pk>/", views.AnalyteDetail.as_view(), name="detail"),

]