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
            'name',
            'parameter',
            'sample',
            'sample_type',
            'condition',
            # 'durations',
            # 'subjects',
            'design_type',
            'design_sample',
            # 'protocol',
            # 'comment',
            # "replicate_count"
            "parameter__reagent_manufacturer",
            "parameter__reagent_name",
            # "parameter__parameter__instrument_manufacturer",
            # "parameter__parameter__instrument_name"
        ]


class ResultFilter(django_filters.FilterSet):

    setting__parameter__parameter__name = django_filters.ModelChoiceFilter(queryset=Parameter.objects.all())

    class Meta:
        model = Result
        fields = [

            'setting__parameter__parameter__name',
            "setting__parameter__instrument__manufacturer",
            "setting__parameter__instrument__name",
            'setting__sample__sample_type',
            'setting__sample__storage',
            'setting__sample__container_additive',
            'setting__sample__gel',
            'setting__condition__temperature',
            'setting__condition__other_condition',
            'setting__parameter__reagent_name',
            'setting__parameter__reagent_manufacturer',
            'setting__parameter__analytical_method',

            'setting__sample_type',
            'setting__design_type',

        ]