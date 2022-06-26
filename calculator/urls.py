
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

    path('settings/', create_setting, name='create-setting'),
    path('settings/setting/<pk>/', setting_detail, name="setting-detail"),
    path('settings/setting/<pk>/delete', delete_setting, name="delete-setting"),
    path('settings/setting/<pk>/edit', edit_setting, name="edit-setting"),
    path('settings/create-setting-form/', add_setting_form, name='create-setting-form'),

    path('conditions/', create_condition, name='create-condition'),
    path('conditions/condition/<pk>/', condition_detail, name="condition-detail"),
    path('conditions/condition/<pk>/delete', delete_condition, name="delete-condition"),
    path('conditions/condition/<pk>/edit', edit_condition, name="edit-condition"),
    path('conditions/create-condition-form/', add_condition_form, name='create-condition-form'),

    path('durations/', create_duration, name='create-duration'),
    path('durations/duration/<pk>/', duration_detail, name="duration-detail"),
    path('durations/duration/<pk>/delete', delete_duration, name="delete-duration"),
    path('durations/duration/<pk>/edit', edit_duration, name="edit-duration"),
    path('durations/create-duration-form/', add_duration_form, name='create-duration-form'),

    path('setting/<setting_pk>/results/', create_result, name='create-result'),
    # path("instrument/<pk>/edit", views.InstrumentUpdateView.as_view(), name="edit_instrument"),
    # path("add-sample/", views.SampleAddView.as_view(), name="add_sample"),
    # path("add-parameter/", views.ParameterAddView.as_view(), name="add_parameter"),
    # path("add-results/", views.ValuesAddView.as_view(), name="add_results"),
    # path("input/", views.MultiInputView.as_view(), name="input"),
    # path("results/<pk>", views.ResultsView.as_view(), name="results"),
    # path("upload/", views.upload_view, name="upload"),



]
