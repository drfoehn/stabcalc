
from django.urls import path
from calculator import views
from calculator.views import *
from django.views.generic import TemplateView


urlpatterns = [

    path('instruments/', create_instrument, name='create-instrument'),
    path('instruments/instrument/<pk>/', instrument_detail, name="instrument-detail"),
    path('instruments/instrument/<pk>/delete', delete_instrument, name="delete-instrument"),
    path('instruments/instrument/<pk>/edit', edit_instrument, name="edit-instrument"),
    path('instruments/create-instrument-form/', add_instrument_form, name='create-instrument-form'),

    path('parameters/', create_parameter, name='create-parameter'),
    path('parameters/parameter/<pk>/', parameter_detail, name="parameter-detail"),
    path('parameters/parameter/<pk>/delete', delete_parameter, name="delete-parameter"),
    path('parameters/parameter/<pk>/edit', edit_parameter, name="edit-parameter"),
    path('parameters/create-parameter-form/', add_parameter_form, name='create-parameter-form'),

    path('samples/', create_sample, name='create-sample'),
    path('samples/sample/<pk>/', sample_detail, name="sample-detail"),
    path('samples/sample/<pk>/delete', delete_sample, name="delete-sample"),
    path('samples/sample/<pk>/edit', edit_sample, name="edit-sample"),
    path('samples/create-sample-form/', add_sample_form, name='create-sample-form'),

    #
    # path("instrument/<pk>/edit", views.InstrumentUpdateView.as_view(), name="edit_instrument"),
    # path("add-sample/", views.SampleAddView.as_view(), name="add_sample"),
    # path("add-parameter/", views.ParameterAddView.as_view(), name="add_parameter"),
    # path("add-results/", views.ValuesAddView.as_view(), name="add_results"),
    # path("input/", views.MultiInputView.as_view(), name="input"),
    # path("results/<pk>", views.ResultsView.as_view(), name="results"),
    # path("upload/", views.upload_view, name="upload"),



]
