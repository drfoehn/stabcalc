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
    CV_intra = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    CV_inter = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    method_hand = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'check-input'}), required=False)
    instrument = forms.ModelChoiceField(queryset=(Instrument.objects.all()), empty_label='Select instrument')

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


class SampleForm(forms.ModelForm):
    sample_type = forms.Select()
    container_additive = forms.Select()
    container_dimension = forms.Select()
    container_fillingvolume = forms.FloatField()
    container_material = forms.Select()
    gel = forms.BooleanField(widget=forms.CheckboxInput(), required=False)

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

    def __init__(self, *args, **kwargs):
        super(SampleForm, self).__init__(*args, **kwargs)
        self.fields['sample_type'].widget.attrs['class'] = 'form-select'
        self.fields['container_dimension'].widget.attrs['class'] = 'form-select'
        self.fields['container_additive'].widget.attrs['class'] = 'form-select'
        self.fields['container_fillingvolume'].widget.attrs['class'] = 'form-control'
        self.fields['container_material'].widget.attrs['class'] = 'form-select'
        self.fields['gel'].widget.attrs['class'] = 'form-check-input'


class SettingForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    parameter = forms.ModelChoiceField(queryset=(Parameter.objects.all()), empty_label='Select parameter')
    condition = forms.ModelChoiceField(queryset=(Condition.objects.all()), empty_label='Select storage condition')
    duration = forms.ModelMultipleChoiceField(queryset=(Duration.objects.all()), widget = forms.CheckboxSelectMultiple)

    # ----------------------Botcatcher-------------------------
    # TODO: Check if working: Bots should not get an error. It should silently fail.
    feedback = forms.CharField(
        widget=forms.HiddenInput,
        required=False,
        validators=[validators.MaxLengthValidator(0)],
    )
    # -----------------------------------------------------------

    class Meta:
        model = Setting
        fields = (
            'name',
            'parameter',
            'condition',
            'duration'
        )

    def __init__(self, *args, **kwargs):
        super(SettingForm, self).__init__(*args, **kwargs)
        self.fields['parameter'].widget.attrs['class'] = 'form-select'
        self.fields['condition'].widget.attrs['class'] = 'form-select'
        self.fields['duration'].widget.attrs['class'] = 'form-check-input'

    # -------------------Botcatcher-------------------------------------
    def clean_feedback(self):
        feedback = self.cleaned_data["feedback"]
        if len(feedback) > 0:
            raise forms.ValidationError("We don´t serve your kind here!")
        return feedback


class ConditionForm(forms.ModelForm):
    temperature = forms.Select()
    light = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    air = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    agitation = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    other_condition = forms.BooleanField(widget=forms.CheckboxInput(), required=False)

    # ----------------------Botcatcher-------------------------
    # TODO: Check if working: Bots should not get an error. It should silently fail.
    feedback = forms.CharField(
        widget=forms.HiddenInput,
        required=False,
        validators=[validators.MaxLengthValidator(0)],
    )
    # -----------------------------------------------------------

    class Meta:
        model = Condition
        fields = (
            'temperature',
            'light',
            'air',
            'agitation',
            'other_condition',
        )

    def __init__(self, *args, **kwargs):
        super(ConditionForm, self).__init__(*args, **kwargs)
        self.fields['temperature'].widget.attrs['class'] = 'form-select'
        self.fields['light'].widget.attrs['class'] = 'form-check-input'
        self.fields['air'].widget.attrs['class'] = 'form-check-input'
        self.fields['agitation'].widget.attrs['class'] = 'form-check-input'
        self.fields['other_condition'].widget.attrs['class'] = 'form-check-input'


    # -------------------Botcatcher-------------------------------------
    def clean_feedback(self):
        feedback = self.cleaned_data["feedback"]
        if len(feedback) > 0:
            raise forms.ValidationError("We don´t serve your kind here!")
        return feedback


class DurationForm(forms.ModelForm):
    duration_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    duration_unit = forms.Select()
    # setting = forms.ModelMultipleChoiceField(queryset=(Duration.objects.all()))


    # ----------------------Botcatcher-------------------------
    # TODO: Check if working: Bots should not get an error. It should silently fail.
    feedback = forms.CharField(
        widget=forms.HiddenInput,
        required=False,
        validators=[validators.MaxLengthValidator(0)],
    )
    # -----------------------------------------------------------

    class Meta:
        model = Duration
        fields = (
            'duration_number',
            'duration_unit',
            # 'setting'
        )

    def __init__(self, *args, **kwargs):
        super(DurationForm, self).__init__(*args, **kwargs)
        self.fields['duration_unit'].widget.attrs['class'] = 'form-select'

    # -------------------Botcatcher-------------------------------------
    def clean_feedback(self):
        feedback = self.cleaned_data["feedback"]
        if len(feedback) > 0:
            raise forms.ValidationError("We don´t serve your kind here!")
        return feedback




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
