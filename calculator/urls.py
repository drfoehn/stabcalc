
from django.urls import path
from calculator import views
from calculator.views import *
from django.views.generic import TemplateView


urlpatterns = [

    # path('', TemplateView.as_view(template_name="calculator/instrument_list.html"), name='create-instrument'),
    path('instruments/', create_instrument, name='create-instrument'),
    path('instruments/instrument/<pk>/', instrument_detail, name="instrument-detail"),
    # path('instrument/<pk>/update/', update_book, name="update-book"),
    # path('instrument/<pk>/delete/', delete_book, name="delete-book"),
    path('instruments/create-instrument-form/', add_instrument_form, name='create-instrument-form'),

    # path('', TemplateView.as_view(template_name="calculator/instrument_list.html"), name='create-instrument'),
    path('parameters/', create_parameter, name='create-parameter'),
    path('parameters/parameter/<pk>/', parameter_detail, name="parameter-detail"),
    # path('instrument/<pk>/update/', update_book, name="update-book"),
    # path('instrument/<pk>/delete/', delete_book, name="delete-book"),
    path('parameters/create-parameter-form/', add_parameter_form, name='create-parameter-form'),


    #
    # path("instrument/<pk>/edit", views.InstrumentUpdateView.as_view(), name="edit_instrument"),
    # path("add-sample/", views.SampleAddView.as_view(), name="add_sample"),
    # path("add-parameter/", views.ParameterAddView.as_view(), name="add_parameter"),
    # path("add-results/", views.ValuesAddView.as_view(), name="add_results"),
    # path("input/", views.MultiInputView.as_view(), name="input"),
    # path("results/<pk>", views.ResultsView.as_view(), name="results"),
    # path("upload/", views.upload_view, name="upload"),



]
