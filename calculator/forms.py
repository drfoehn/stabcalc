from django.core import validators
from django.forms import formset_factory, modelformset_factory

from .models import *
from django import forms

# TODO: https://pypi.org/project/django-composite-field/;  https://pypi.org/project/django-dynamic-admin-forms/

class InstrumentForm(forms.ModelForm):
    class Meta:
        model = Instrument
        fields = ('name','manufacturer')


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

# class ValueForm(forms.ModelForm):
#     class Meta:
#         model = Value
#         fields = '__all__'
#
# ValueFormset = modelformset_factory(Subject, fields=("duration",), extra=1)



