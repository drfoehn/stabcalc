import django_filters
from .models import *
from django.db import models
from django import forms


class AnalyteFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    class Meta:
        model = Analyte
        fields = [
            "name",
        ]
