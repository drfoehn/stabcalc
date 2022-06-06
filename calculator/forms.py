from django.core import validators
from .models import *
from django import forms


class InstrumentForm(forms.ModelForm):
    class Meta:
        model = Instrument
        fields = '__all__'



class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = '__all__'


class ParameterForm(forms.ModelForm):
    class Meta:
        model = Parameter
        fields = '__all__'

