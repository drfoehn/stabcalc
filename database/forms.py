from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import *
from django import forms


class AnalyteSpecimenSearchForm(forms.ModelForm):
    analyte = forms.ModelChoiceField(queryset=(AnalyteSpecimen.objects.all()))

    # ----------------------Botcatcher-------------------------

    feedback = forms.CharField(
        widget=forms.HiddenInput,
        required=False,
        validators=[validators.MaxLengthValidator(0)],
    )
    # -----------------------------------------------------------

    class Meta:
        model = AnalyteSpecimen
        fields = (
            'analyte',
            'specimen'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['analyte'].widget.attrs['class'] = 'form-select'



    # -------------------Botcatcher-------------------------------------
    def clean_feedback(self):
        feedback = self.cleaned_data["feedback"]
        if len(feedback) > 0:
            raise forms.ValidationError("We don´t serve your kind here!")
        return feedback