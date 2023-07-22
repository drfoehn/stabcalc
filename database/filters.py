import django_filters
from .models import *
from django import template
from django.db import models
from django import forms


class AnalyteFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    class Meta:
        model = Analyte
        fields = [
            "name",
        ]




register = template.Library()

@register.filter
def time_format(value):
    if value < 60:
        return f"{value} minutes"
    elif value < 3600:
        return f"{value // 60} hours"
    else:
        return f"{value // 3600} hours"


