
from django.urls import path
from calculator import views
from calculator.views import *
from django.views.generic import TemplateView


urlpatterns = [

    path('instruments/', instrument_list, name='create-instrument'),
    path('instruments/instrument/<pk>/', instrument_detail, name="instrument-detail"),
    path('instruments/instrument/<pk>/delete', delete_instrument, name="delete-instrument"),
    path('instruments/instrument/<pk>/edit', edit_instrument, name="edit-instrument"),
    path('instruments/create-instrument-form/', add_instrument_form, name='create-instrument-form'),

    path('parameters/', parameter_list, name='create-parameter'),
    path('parameters/parameter/<pk>/', parameter_detail, name="parameter-detail"),
    path('parameters/parameter/<pk>/delete', delete_parameter, name="delete-parameter"),
    path('parameters/parameter/<pk>/edit', edit_parameter, name="edit-parameter"),
    path('parameters/create-parameter-form/', add_parameter_form, name='create-parameter-form'),
    path('parameters/search', search_parameter, name='search-parameter'),

    path('samples/', sample_list, name='create-sample'),
    path('samples/sample/<pk>/', sample_detail, name="sample-detail"),
    path('samples/sample/<pk>/delete', delete_sample, name="delete-sample"),
    path('samples/sample/<pk>/edit', edit_sample, name="edit-sample"),
    path('samples/create-sample-form/', add_sample_form, name='create-sample-form'),

    path('settings/', setting_list, name='create-setting'),
    path('settings/setting/<pk>/', setting_detail, name="setting-detail"),
    path('settings/setting/<pk>/delete', delete_setting, name="delete-setting"),
    path('settings/setting/<pk>/edit', edit_setting, name="edit-setting"),
    path('settings/create-setting-form/', add_setting_form, name='create-setting-form'),

    path('conditions/', condition_list, name='create-condition'),
    path('conditions/condition/<pk>/', condition_detail, name="condition-detail"),
    path('conditions/condition/<pk>/delete', delete_condition, name="delete-condition"),
    path('conditions/condition/<pk>/edit', edit_condition, name="edit-condition"),
    path('conditions/create-condition-form/', add_condition_form, name='create-condition-form'),

    path('preanalytical-sets/', preanalytical_set_list, name='create-preanalytical-set'),
    path('preanalytical-sets/preanalytical-set/<pk>/', preanalytics_detail, name="preanalytical-set-detail"),
    path('preanalytical-sets/preanalytical-set/<pk>/delete', delete_preanalytical_set, name="delete-preanalytical-set"),
    path('preanalytical-sets/preanalytical-set/<pk>/edit', edit_preanalytical_set, name="edit-preanalytical-set"),
    path('preanalytical-sets/create-preanalytical-set-form/', add_preanalytics_form, name='create-preanalytical-set-form'),

    path('durations/', duration_list, name='create-duration'),
    path('durations/duration/<pk>/', duration_detail, name="duration-detail"),
    path('durations/duration/<pk>/delete', delete_duration, name="delete-duration"),
    path('durations/duration/<pk>/edit', edit_duration, name="edit-duration"),
    path('durations/create-duration-form/', add_duration_form, name='create-duration-form'),

    path('subjects/', subject_list, name='create-subject'),
    path('subjects/subject/<pk>/', subject_detail, name="subject-detail"),
    path('subjects/subject/<pk>/delete', delete_subject, name="delete-subject"),
    path('subjects/subject/<pk>/edit', edit_subject, name="edit-subject"),
    path('subjects/create-subject-form/', add_subject_form, name='create-subject-form'),

    path('setting/<setting_pk>/results/', result_list, name='create-result'),
    path('results/result/<pk>/', result_detail, name="result-detail"),
    path('results/result/<pk>/delete', delete_result, name="delete-result"),
    path('results/result/<pk>/edit', edit_result, name="edit-result"),
    path('results/create-result-form/<setting_pk>/<duration_pk>', add_result_form, name='create-result-form'),

    path("results/<pk>", views.ResultsView.as_view(), name="results"),

    path("download-xlsx", views.DownloadExcel, name="download-data")
    # path("upload/", views.upload_view, name="upload"),





]
