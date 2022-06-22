from django.core import validators
from django.forms import formset_factory, modelformset_factory
from django.http import request

from .models import *
from django import forms

#https://django-addanother.readthedocs.io/en/latest/
#https://github.com/trco/django-funky-sheets/blob/master/README.rst

# TODO: https://pypi.org/project/django-composite-field/;  https://pypi.org/project/django-dynamic-admin-forms/

class InstrumentForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    manufacturer = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Instrument
        fields = ('name', 'manufacturer')


class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = '__all__'


class ParameterForm(forms.ModelForm):
    class Meta:
        model = Parameter
        fields = '__all__'


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



