from django.contrib import admin
from django.urls import path, include
from database import views
from database.views import *

# from calculator.admin import user_dashboard
# from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


urlpatterns = [
    path("search/", search_analyte, name="search_analyte"),
    path("", views.AnalyteSpecimenIndex.as_view(), name="analytespecimen_list"),
    path("<int:pk>/", views.AnalyteDetail.as_view(), name="analyte_detail"),
    path('category/<int:pk>/analytes/', views.CategoryAnalytesView.as_view(), name='analyte_list_by_category'),
    # path("<int:pk>/blood", views.AnalyteDetail.as_view(), name="analyte_blood"),
    # path('analytes/<pk>/select', select_analyte, name='select-analyte'),
]