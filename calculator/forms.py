from django.core import validators
from django.forms import formset_factory, modelformset_factory
from django.http import request

from .models import *
from django import forms


# https://django-addanother.readthedocs.io/en/latest/
# https://github.com/trco/django-funky-sheets/blob/master/README.rst

# TODO: https://pypi.org/project/django-composite-field/;  https://pypi.org/project/django-dynamic-admin-forms/

class InstrumentForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    manufacturer = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Instrument
        fields = (
            'name',
            'manufacturer',
        )


class ParameterForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    unit = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    reagent_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    reagent_manufacturer = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    CV_intra = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    CV_inter = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    method_hand = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'check-input'}))
    instrument = forms.ModelChoiceField(queryset=(Instrument.objects.filter()), empty_label='Select instrument')

    # instrument = models.ForeignKey(Instrument)
    # sample = models.ForeignKey(Sample)

    # ----------------------Botcatcher-------------------------
    # TODO: Check if working: Bots should not get an error. It should silently fail.
    feedback = forms.CharField(
        widget=forms.HiddenInput,
        required=False,
        validators=[validators.MaxLengthValidator(0)],
    )
    # -----------------------------------------------------------

    class Meta:
        model = Parameter
        fields = (
            'name',
            'unit',
            'reagent_name',
            'reagent_manufacturer',
            'CV_intra',
            'CV_inter',
            'method_hand',
            'instrument',
        )

    def __init__(self, *args, **kwargs):
        super(ParameterForm, self).__init__(*args, **kwargs)
        self.fields['instrument'].widget.attrs['class'] = 'form-select'


    # -------------------Botcatcher-------------------------------------
    def clean_feedback(self):
        feedback = self.cleaned_data["feedback"]
        if len(feedback) > 0:
            raise forms.ValidationError("We don´t serve your kind here!")
        return feedback


class SampleForm(forms.Form):
    sample_type = forms.ChoiceField()
    container_additive = forms.ChoiceField()
    container_dimension = forms.ChoiceField()
    container_fillingvolume = forms.FloatField()
    container_material = forms.ChoiceField()
    gel = forms.BooleanField()

    class Meta:
        model = Sample
        fields = (
            'sample_type',
            'container_additive',
            'container_dimension',
            'container_fillingvolume',
            'container_material',
            'gel',
        )


class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = '__all__'


class DurationForm(forms.ModelForm):
    class Meta:
        model = Duration
        fields = '__all__'


class UploadExcelForm(forms.Form):
    stability_data_excel = forms.FileField(
        label='Upload Excel File',
        help_text='Please be sure to use the correct template and filetype'
    )

# class ValueForm(forms.ModelForm):
#     class Meta:
#         model = Value
#         fields = '__all__'
#
# ValueFormset = modelformset_factory(Subject, fields=("duration",), extra=1)
