import django_filters
from calculator.models import *
from django.db import models
from django import forms


class SettingFilter(django_filters.FilterSet):
    # Filter doenst with checkboxselectmultiple widget -  the answer is "Bitte eine gültige Auswahl treffen. ['3'] ist keine gültige Auswahl."
    # name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    # parameter = django_filters.ModelChoiceFilter(queryset=Parameter.objects.all())
    # sample = django_filters.ModelChoiceFilter(queryset=Sample.objects.all())
    # sample_type= django_filters.ChoiceFilter(
    #     field_name="sample_type",
    #     choices=Setting.sample_type.choices
    #                                          )
    # condition= django_filters.ModelChoiceFilter(queryset=Condition.objects.all())
    # design_sample= django_filters.ChoiceFilter(
    #     field_name="design_sample",
    #     choices=Setting.design_sample.choices
    #                                          )
    #
    #
    #
    # tags = django_filters.ModelMultipleChoiceFilter(
    #     queryset=HikeTag.objects.all(), widget=forms.CheckboxSelectMultiple
    # )
    #
    # duration = django_filters.ChoiceFilter(
    #     field_name="duration",
    #     choices=Hike.Duration.choices
    #     # , empty_label=None
    # )
    #
    # shadow = django_filters.ChoiceFilter(
    #     field_name="shadow",
    #     choices=Hike.Shadow.choices
    #     # , empty_label=None
    # )
    #
    # difficulty = django_filters.ChoiceFilter(
    #     field_name="difficulty",
    #     choices=Hike.Difficulty.choices
    #     # , empty_label=None
    # )
    #
    #


    class Meta:
        model = Setting
        fields = [
            # 'name',
            'parameter',
            'sample',
            # 'sample_type',
            'condition',
            # 'design_sample',
        ]


