import django_filters
from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Reset, Layout

from calculator.models import *
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import default
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

    SAMPLETYPE = (
        # (None, _("All")),
        (1, _("Venous Blood")),
        (2, _("Capillary Blood")),
        (3, _("Arterial Blood")),
        (4, _("Urine")),
        (5, _("CSF")),
        (6, _("Stool")),
        (7, _("Other - Please specify")),
    )

    STORAGE = (
        (1, _("Whole Blood")),
        (2, _("Plasma/Serum")),
    )

    CONTAINERADDITIVE = (
        (0, _("No additive")),
        (1, _("EDTA")),
        (2, _("Heparin")),
        (3, _("Citrate")),
        (4, _("Clotactivator (Serum)")),
        (5, _("Other - Please specify")),
    )

    GEL = (
        (0, 'False'),
        (1, 'True'),
    )

    TYPE = (
        (1, _("Patients")),
        (2, _("Healthy volunteers")),
        (3, _("Other")),
    )

    DESIGN_SAMPLE = (
        (1, _("primary samples")),
        (2, _("aliquots")),
    )

    TEMPERATURE = (
        (1, _("Roomtemperature (20 to 25°C)")),
        (2, _("Refrigerated (2 to 6°C)")),
        (3, _("Frozen (-15 to -25°C)")),
        (4, _("Deepfrozen (-60 to -80°C)")),
        (5, _("Other - Please specify")),

    )

    setting__parameter__parameter__name = django_filters.ModelChoiceFilter(
        queryset=Parameter.objects.all(),
        label = "Select Parameter"
    )
    setting__parameter__instrument__manufacturer = django_filters.CharFilter(
        field_name="setting__parameter__instrument__manufacturer",
        lookup_expr='icontains',
        label="Analytical Instrument Manufacturer Name contains"
    )
    setting__parameter__instrument__name  = django_filters.CharFilter(
        field_name="setting__parameter__instrument__name",
        lookup_expr='icontains',
        label="Analytical Instrument Name contains"
    )
    setting__sample__sample_type = django_filters.TypedMultipleChoiceFilter(
        field_name="setting__sample__sample_type",
        choices=SAMPLETYPE,
        widget=forms.CheckboxSelectMultiple,
        label="Sample type / Matrix"
    )
    setting__sample__storage = django_filters.TypedMultipleChoiceFilter(
        field_name="setting__sample__storage",
        choices=STORAGE,
        widget=forms.CheckboxSelectMultiple,
        label="Samples stored as"
    )
    setting__sample__container_additive = django_filters.TypedMultipleChoiceFilter(
        field_name="setting__sample__container_additive",
        choices=CONTAINERADDITIVE,
        widget=forms.CheckboxSelectMultiple,
        label="Collection tube additive"
    )
    setting__sample__gel = django_filters.TypedMultipleChoiceFilter(
        field_name="setting__sample__gel",
        choices=GEL,
        widget=forms.CheckboxSelectMultiple,
        label="Storage in Sample with gel?"
    )
    setting__condition__temperature = django_filters.TypedMultipleChoiceFilter(
        field_name="setting__condition__temperature",
        choices=TEMPERATURE,
        widget=forms.CheckboxSelectMultiple,
        label="Storage temperature"
    )
    setting__condition__other_condition = django_filters.CharFilter(
        field_name="setting__condition__other_condition",
        lookup_expr='icontains',
        label="Other storage condition contains"
    )
    setting__parameter__reagent_name = django_filters.CharFilter(
        field_name="setting__parameter__reagent_name",
        lookup_expr='icontains',
        label="Assay Name contains"
    )
    setting__parameter__reagent_manufacturer = django_filters.CharFilter(
        field_name="setting__parameter__reagent_manufacturer",
        lookup_expr='icontains',
        label="Assay Manufacturer contains"
    )
    setting__parameter__analytical_method = django_filters.CharFilter(
        field_name="setting__parameter__analytical_method",
        lookup_expr='icontains',
        label="Analytical Method contains"
    )
    setting__sample_type = django_filters.TypedMultipleChoiceFilter(
        field_name="setting__sample_type",
        choices=TYPE,
        widget=forms.CheckboxSelectMultiple,
        label="Type of study subjects"
    )
    setting__design_sample = django_filters.TypedMultipleChoiceFilter(
        field_name="setting__design_sample",
        choices=DESIGN_SAMPLE,
        widget=forms.CheckboxSelectMultiple,
        label="Samples stored in"
    )


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
            'setting__design_sample',

        ]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)
    #     self.helper.form_id = 'results_search_form'
    #     self.helper.form_class = 'search-filter-form mb-4'
    #     self.helper.form_method = 'GET'
    #     self.helper.use_custom_control = True
    #     self.helper.label_class = 'font-wight-bold'
    #
    #     self.helper.add_input(Submit('submit', 'Submit', css_class='btn btn-wide btn-dark-custom mr-3'))
    #     self.helper.add_input(Reset('clear-search', 'Clear Filters', css_class='btn btn-wide btn-light'))
    #
    #     self.helper.layout = Layout(
    #         # Row(
    #         #     Column('email', css_class='form-group col-md-6 mb-0'),
    #         #     Column('password', css_class='form-group col-md-6 mb-0'),
    #         #     css_class='form-row'
    #         # ),
    #         # 'search_text',
    #         # InlineCheckboxes('One', css_class="checkboxes-filter-form"),
    #         # InlineCheckboxes('Two', css_class="checkboxes-filter-form"),
    #         # InlineCheckboxes('Three', css_class="checkboxes-filter-form"),
    #     )