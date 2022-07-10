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
    # instrument = forms.ModelChoiceField(queryset=(Instrument.objects.all()), empty_label='Select instrument')

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
        user = kwargs.pop('user')   #get the correct user for the dropdown-selections
        self.owner = user  # retrieve the current user, so that the dropdown of foreignkeys only shows the users own objects
        super().__init__(*args, **kwargs)
        self.fields['instrument'].queryset = Instrument.objects.filter(owner=user)
        self.fields['instrument'].widget.attrs['class'] = 'form-select'


    # -------------------Botcatcher-------------------------------------
    def clean_feedback(self):
        feedback = self.cleaned_data["feedback"]
        if len(feedback) > 0:
            raise forms.ValidationError("We don´t serve your kind here!")
        return feedback


class SampleForm(forms.ModelForm):
    sample_type = forms.Select()
    sample_type_other = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sample_leftover = forms.BooleanField(widget=forms.CheckboxInput())
    sample_pool = forms.BooleanField(widget=forms.CheckboxInput())
    sample_pool_text = forms.CharField(max_length=400, widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    sample_spike = forms.BooleanField(widget=forms.CheckboxInput())
    sample_spike_text = forms.CharField(max_length=400, widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    container_additive = forms.Select()
    container_additive_other = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    container_dimension = forms.Select()
    container_dimension_other = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    container_fillingvolume = forms.FloatField(required=False)
    container_material = forms.Select()
    container_material_other = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    gel = forms.BooleanField(widget=forms.CheckboxInput(), required=False)

    class Meta:
        model = Sample
        fields = (
            'sample_type',
            'sample_type_other',
            'sample_leftover',
            'sample_pool',
            'sample_pool_text',
            'sample_spike',
            'sample_spike_text',
            'container_additive',
            'container_additive_other',
            'container_dimension',
            'container_dimension_other',
            'container_fillingvolume',
            'container_material',
            'container_material_other',
            'gel',
        )

    def __init__(self, *args, **kwargs):
        super(SampleForm, self).__init__(*args, **kwargs)
        self.fields['sample_type'].widget.attrs['class'] = 'form-select'
        self.fields['sample_type'].widget.attrs['onchange'] = "showMe(\"idShowMe\")"
        self.fields['container_dimension'].widget.attrs['class'] = 'form-select'
        self.fields['container_additive'].widget.attrs['class'] = 'form-select'
        self.fields['container_fillingvolume'].widget.attrs['class'] = 'form-control'
        self.fields['container_material'].widget.attrs['class'] = 'form-select'
        self.fields['gel'].widget.attrs['class'] = 'form-check-input'
        self.fields['sample_spike'].widget.attrs['class'] = 'form-check-input'
        self.fields['sample_pool'].widget.attrs['class'] = 'form-check-input'
        self.fields['sample_leftover'].widget.attrs['class'] = 'form-check-input'



class SettingForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    parameter = forms.ModelChoiceField(queryset=Parameter.objects.all(), empty_label='---Select parameter---')
    condition = forms.ModelChoiceField(queryset=Condition.objects.all(), empty_label='---Select storage condition---')
    comment = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    owner = None
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
            'duration',
            'subject',
            'comment'
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')   #get the correct user for the dropdown-selections
        self.owner = user  # retrieve the current user, so that the dropdown of foreignkeys only shows the users own objects

        super().__init__(*args, **kwargs)
        # self.fields['subject'].queryset = Subject.objects.filter(owner=user)
        self.fields['duration'] = forms.ModelMultipleChoiceField(
            Duration.objects.filter(owner=user),
            widget=forms.CheckboxSelectMultiple,
        )
        self.fields['subject'] = forms.ModelMultipleChoiceField(
            queryset=Subject.objects.filter(owner=user),
            widget=forms.CheckboxSelectMultiple,
        )
        self.fields['parameter'].widget.attrs['class'] = 'form-select'
        self.fields['condition'].widget.attrs['class'] = 'form-select'


    def get_subjects_queryset(self):
        return Subject.objects.filter(owner=self.owner)

    # -------------------Botcatcher-------------------------------------
    def clean_feedback(self):
        feedback = self.cleaned_data["feedback"]
        if len(feedback) > 0:
            raise forms.ValidationError("We don´t serve your kind here!")
        return feedback


class ConditionForm(forms.ModelForm):
    temperature = forms.Select()
    temperature_other = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    light = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    air = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    agitation = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    thawing = forms.CharField(max_length=400, widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    other_condition = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))

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
            'temperature_other',
            'light',
            'air',
            'agitation',
            'thawing',
            'other_condition',
        )

    def __init__(self, *args, **kwargs):
        super(ConditionForm, self).__init__(*args, **kwargs)
        self.fields['temperature'].widget.attrs['class'] = 'form-select'
        self.fields['light'].widget.attrs['class'] = 'form-check-input'
        self.fields['air'].widget.attrs['class'] = 'form-check-input'
        self.fields['agitation'].widget.attrs['class'] = 'form-check-input'





    # -------------------Botcatcher-------------------------------------
    def clean_feedback(self):
        feedback = self.cleaned_data["feedback"]
        if len(feedback) > 0:
            raise forms.ValidationError("We don´t serve your kind here!")
        return feedback


class DurationForm(forms.ModelForm):
    duration_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    duration_unit = forms.Select()


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


class SubjectForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # setting = forms.ModelMultipleChoiceField(queryset=(Setting.objects.all()))


    class Meta:
        model = Subject
        fields = (
            'name',
            # 'setting',

        )

    # def __init__(self, *args, **kwargs):
    #     super(SubjectForm, self).__init__(*args, **kwargs)
        # self.fields['setting'].widget.attrs['class'] = 'form-check-input'

    # -------------------Botcatcher-------------------------------------
    def clean_feedback(self):
        feedback = self.cleaned_data["feedback"]
        if len(feedback) > 0:
            raise forms.ValidationError("We don´t serve your kind here!")
        return feedback


class ResultForm(forms.Form):
    # value = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    # setting = forms.ModelChoiceField(queryset=Setting.objects.all(), required=False)
    # duration = forms.ModelChoiceField(queryset=Duration.objects.all(), required=False)
    # subject = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), required=False)
    # subject = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)

    # class Meta:
    #     model = Result
    #     fields = (
    #         'value',
    #         'setting',
    #         'duration',
    #         'subject'
    #     )

    def __init__(self, subjects, durations, *args,**kwargs):
        super().__init__(*args,**kwargs)
        for subject in subjects:
            for duration in durations:
                field = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
                field.subject_id = subject.id
                field.duration_id = duration.id
                self.fields[f"value-{subject.id}-{duration.id}"] = field

    # -------------------Botcatcher-------------------------------------
    def clean_feedback(self):
        feedback = self.cleaned_data["feedback"]
        if len(feedback) > 0:
            raise forms.ValidationError("We don´t serve your kind here!")
        return feedback

    # def __init__(self, *args, **kwargs):
    #     super(ResultForm, self).__init__(*args, **kwargs)
    #     self.fields['subject'].widget.attrs['class'] = 'form-check-input'


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
