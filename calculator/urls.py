
from django.urls import path
from calculator import views
from calculator.views import *


urlpatterns = [

    path("add-instrument/", views.InstrumentAddView, name="add_instrument"),
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
