from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import formset_factory, modelformset_factory
from django.http import request
from django.utils.translation import gettext_lazy as _
from .models import *
from django import forms


# https://django-addanother.readthedocs.io/en/latest/
# https://github.com/trco/django-funky-sheets/blob/master/README.rst

# TODO: https://pypi.org/project/django-composite-field/;  https://pypi.org/project/django-dynamic-admin-forms/



class InstrumentForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    manufacturer = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    feedback = forms.CharField(
        widget=forms.HiddenInput,
        required=False,
        validators=[validators.MaxLengthValidator(0)],
    )
    class Meta:
        model = Instrument
        fields = (
            'name',
            'manufacturer',
        )

    def clean_feedback(self):
        feedback = self.cleaned_data["feedback"]
        if len(feedback) > 0:
            raise forms.ValidationError("We don´t serve your kind here!")
        return feedback


class ParameterUserForm(forms.ModelForm):
    parameter = forms.ModelChoiceField(queryset=(Parameter.objects.all()))
    reagent_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    reagent_manufacturer = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    analytical_method = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    method_hand = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'check-input'}), required=False)
    instrument = forms.ModelChoiceField(queryset=(Instrument.objects.all()), empty_label='Select instrument', required=False)
    cv_a = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    #
    # instrument = models.ForeignKey(Instrument)
    # sample = models.ForeignKey(Sample)
    #
    # ----------------------Botcatcher-------------------------

    feedback = forms.CharField(
        widget=forms.HiddenInput,
        required=False,
        validators=[validators.MaxLengthValidator(0)],
    )
    # -----------------------------------------------------------

    class Meta:
        model = ParameterUser
        fields = (
            'parameter',
            'reagent_name',
            'reagent_manufacturer',
            'analytical_method',
            'method_hand',
            'instrument',
            'cv_a'
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')   #get the correct user for the dropdown-selections
        self.owner = user  # retrieve the current user, so that the dropdown of foreignkeys only shows the users own objects
        super().__init__(*args, **kwargs)
        self.fields['instrument'].queryset = Instrument.objects.filter(owner=user)
        self.fields['instrument'].widget.attrs['class'] = 'form-select'
        self.fields['parameter'].widget.attrs['class'] = 'form-select'



    # -------------------Botcatcher-------------------------------------
    def clean_feedback(self):
        feedback = self.cleaned_data["feedback"]
        if len(feedback) > 0:
            raise forms.ValidationError("We don´t serve your kind here!")
        return feedback


class SampleForm(forms.ModelForm):

    sample_type = forms.Select()
    sample_type_other = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    storage = forms.Select()
    sample_leftover = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    sample_pool = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    sample_pool_text = forms.CharField(max_length=400, widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    sample_spike = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    sample_spike_text = forms.CharField(max_length=400, widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    container_additive = forms.Select(attrs={'required': False})
    container_additive_other = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    container_dimension = forms.Select(attrs={'required': False})
    container_dimension_other = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    container_fillingvolume = forms.FloatField(required=False)
    container_material = forms.Select(attrs={'required': False})
    container_material_other = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    gel = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    preanalytical_set = forms.ModelChoiceField(queryset=PreanalyticalSet.objects.all(), empty_label='---Select preanalytical set---')

    # owner = None

    # ----------------------Botcatcher-------------------------

    feedback = forms.CharField(
        widget=forms.HiddenInput,
        required=False,
        validators=[validators.MaxLengthValidator(0)],
    )
    # -----------------------------------------------------------

    class Meta:
        model = Sample
        fields = (
            'sample_type',
            'sample_type_other',
            'storage',
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
            'preanalytical_set',
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # get the correct user for the dropdown-selections
        self.owner = user  # retrieve the current user, so that the dropdown of foreignkeys only shows the users own objects
        super().__init__(*args, **kwargs)
        self.fields['sample_type'].widget.attrs['class'] = 'form-select'
        self.fields['sample_type'].widget.attrs['onchange'] = "showMe(\"idShowMe\")"
        self.fields['storage'].widget.attrs['class'] = 'form-select'
        self.fields['container_dimension'].widget.attrs['class'] = 'form-select'
        self.fields['container_additive'].widget.attrs['class'] = 'form-select'
        self.fields['container_fillingvolume'].widget.attrs['class'] = 'form-control'
        self.fields['container_material'].widget.attrs['class'] = 'form-select'
        self.fields['gel'].widget.attrs['class'] = 'form-check-input'
        self.fields['sample_spike'].widget.attrs['class'] = 'form-check-input'
        self.fields['sample_pool'].widget.attrs['class'] = 'form-check-input'
        self.fields['sample_leftover'].widget.attrs['class'] = 'form-check-input'
        self.fields['preanalytical_set'].queryset = PreanalyticalSet.objects.filter(owner=user)
        self.fields['preanalytical_set'].widget.attrs['class'] = 'form-select'

    def clean_feedback(self):
        feedback = self.cleaned_data["feedback"]
        if len(feedback) > 0:
            raise forms.ValidationError("We don´t serve your kind here!")
        return feedback


class PreanalyticalSetForm(forms.ModelForm):
    collection_instrument = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    collection_site =forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    transportation_temp = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    transportation_method = forms.Select()
    transportation_method_other = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    transportation_time_unit = forms.Select()
    transportation_time = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    centrifugation_g = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    centrifugation_time = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    centrifugation_temp = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    comment = forms.Textarea(attrs={'class': 'form-control'})
    feedback = forms.CharField(
        widget=forms.HiddenInput,
        required=False,
        validators=[validators.MaxLengthValidator(0)],
    )

    class Meta:
        model = PreanalyticalSet
        fields = (
        'collection_instrument',
        'collection_site',
        'transportation_temp',
        'transportation_method',
        'transportation_method_other',
        'transportation_time_unit',
        'transportation_time',
        'centrifugation_g' ,
        'centrifugation_time',
        'centrifugation_temp',
        'comment',
        )

    def __init__(self, *args, **kwargs):
        super(PreanalyticalSetForm, self).__init__(*args, **kwargs)
        self.fields['collection_instrument'].widget.attrs['placeholder'] = 'e.g. Butterfly, Needle, None, ...'
        self.fields['collection_site'].widget.attrs['placeholder'] = 'e.g. Cubital vein'
        self.fields['transportation_time_unit'].widget.attrs['class'] = 'form-select'
        self.fields['transportation_method'].widget.attrs['class'] = 'form-select'

    def clean_feedback(self):
        feedback = self.cleaned_data["feedback"]
        if len(feedback) > 0:
            raise forms.ValidationError("We don´t serve your kind here!")
        return feedback


class SettingForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    parameter = forms.ModelChoiceField(queryset=ParameterUser.objects.all(), empty_label='---Select parameter---')
    sample = forms.ModelChoiceField(queryset=Sample.objects.all(), empty_label='---Select sample---')
    durations = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)
    sample_type = forms.Select()
    freeze_thaw = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    design_type = forms.Select()
    design_sample = forms.Select()
    replicate_count = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)
    condition = forms.ModelChoiceField(queryset=Condition.objects.all(), empty_label='---Select storage condition---')
    protocol = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    comment = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)

    owner = None
    # ----------------------Botcatcher-------------------------

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
            'sample',
            'sample_type',
            'freeze_thaw',
            'condition',
            'durations',
            'subjects',
            'design_type',
            'design_sample',
            'protocol',
            'comment',
            "replicate_count"
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')   #get the correct user for the dropdown-selections
        self.owner = user  # retrieve the current user, so that the dropdown of foreignkeys only shows the users own objects

        super().__init__(*args, **kwargs)

        self.fields['durations'].queryset = Duration.objects.filter(owner=user)
        # self.fields['durations'].widget = forms.CheckboxSelectMultiple
        self.fields['subjects'] = forms.ModelMultipleChoiceField(
            queryset=Subject.objects.filter(owner=user),
            widget=forms.CheckboxSelectMultiple,
        )
        self.fields['sample'] = forms.ModelChoiceField(
            queryset=Sample.objects.filter(owner=user),
            widget=forms.Select,
        )
        self.fields['parameter'].widget.attrs['class'] = 'form-select'
        self.fields['parameter'].queryset = ParameterUser.objects.filter(owner=user)
        self.fields['condition'].widget.attrs['class'] = 'form-select'
        self.fields['condition'].queryset = Condition.objects.filter(owner=user)
        self.fields['sample'].widget.attrs['class'] = 'form-select'
        self.fields['sample_type'].widget.attrs['class'] = 'form-select'
        self.fields['design_sample'].widget.attrs['class'] = 'form-select'
        self.fields['design_type'].widget.attrs['class'] = 'form-select'
        # self.fields['sample'].widget.attrs['class'] = 'form-select'

    def clean_durations(self):
        data = self.cleaned_data['durations']
        found = False
        objects = Duration.objects.filter(id__in=data)
        for d in objects:
            if d.seconds == 0:
                found = True
                break
        if not found:
            raise ValidationError("Storage durations 0 Minutes required (Baseline)")
        return data

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
    light = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    air = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    cell = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    agitation = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    thawing = forms.CharField(max_length=400, widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    other_condition = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}),  required=False)

    # ----------------------Botcatcher-------------------------

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
            'cell',
            'agitation',
            'thawing',
            'other_condition',
        )

    def __init__(self, *args, **kwargs):
        super(ConditionForm, self).__init__(*args, **kwargs)
        self.fields['temperature'].widget.attrs['class'] = 'form-select'
        self.fields['light'].widget.attrs['class'] = 'form-check-input'
        self.fields['air'].widget.attrs['class'] = 'form-check-input'
        self.fields['cell'].widget.attrs['class'] = 'form-check-input'
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


class SubjectForm(forms.Form):
    number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    subject_prefix = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    feedback = forms.CharField(
        widget=forms.HiddenInput,
        required=False,
        validators=[validators.MaxLengthValidator(0)],
    )


    # class Meta:
    #     model = Subject
    #     fields = (
    #         'number',
    #         'subject_prefix',
    #         'name',
    #         # 'setting',
    #
    #     )

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


class ResultTemplateUploadForm(forms.Form):
    result_template_upload_file = forms.FileField(
        label='Upload Excel File with your results',
        help_text='Please be sure to use the correct template and filetype (.xlsx)'
    )



    # class Meta:
    #
    #     model = Result
    #     fields = (
    #         'value',
    #         'setting',
    #         'duration',
    #         'subject',
    #
    #     )


class NewParameterForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    unit = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cv_a = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    cv_i = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    cv_g = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    user = forms.CharField(max_length=255, widget=forms.HiddenInput(), required=False)
    email = forms.EmailField(widget=forms.HiddenInput(), required=False)

    class Meta:
        fields = (
            'name',
            'unit',
            'cv_g',
            'cv_i',
            'cv_a',
            'email'

        )

    def save(self, commit):
        pass

# class SettingAdminForm(forms.ModelForm):
#     # name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     parameter = forms.ModelChoiceField(queryset=Parameter.objects.all(), empty_label='---Select parameter---')
#     sample = forms.ModelChoiceField(queryset=Sample.objects.all(), empty_label='---Select sample---')
#     # durations = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)
#     sample_type = forms.Select()
#     # freeze_thaw = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
#     design_type = forms.Select()
#     design_sample = forms.Select()
#     instrument_name = forms.Ch
#     # replicate_count = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)
#     # condition = forms.ModelChoiceField(queryset=Condition.objects.all(), empty_label='---Select storage condition---')
#     # protocol = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
#     # comment = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
#
#     owner = None
#     # ----------------------Botcatcher-------------------------
#
#     feedback = forms.CharField(
#         widget=forms.HiddenInput,
#         required=False,
#         validators=[validators.MaxLengthValidator(0)],
#     )
#     # -----------------------------------------------------------
#
#     class Meta:
#         model = Setting
#         fields = (
#             'name',
#             'parameter',
#             'sample',
#             'sample_type',
#             'freeze_thaw',
#             'condition',
#             'durations',
#             'subjects',
#             'design_type',
#             'design_sample',
#             'protocol',
#             'comment',
#             "replicate_count"
#         )
#
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user')   #get the correct user for the dropdown-selections
#         self.owner = user  # retrieve the current user, so that the dropdown of foreignkeys only shows the users own objects
#
#         super().__init__(*args, **kwargs)
#
#         self.fields['durations'].queryset = Duration.objects.filter(owner=user)
#         # self.fields['durations'].widget = forms.CheckboxSelectMultiple
#         self.fields['subjects'] = forms.ModelMultipleChoiceField(
#             queryset=Subject.objects.filter(owner=user),
#             widget=forms.CheckboxSelectMultiple,
#         )
#         self.fields['sample'] = forms.ModelChoiceField(
#             queryset=Sample.objects.filter(owner=user),
#             widget=forms.Select,
#         )
#         self.fields['parameter'].widget.attrs['class'] = 'form-select'
#         self.fields['condition'].widget.attrs['class'] = 'form-select'
#         self.fields['sample'].widget.attrs['class'] = 'form-select'
#         self.fields['sample_type'].widget.attrs['class'] = 'form-select'
#         self.fields['design_sample'].widget.attrs['class'] = 'form-select'
#         self.fields['design_type'].widget.attrs['class'] = 'form-select'
#         # self.fields['sample'].widget.attrs['class'] = 'form-select'
#
#     def clean_durations(self):
#         data = self.cleaned_data['durations']
#         found = False
#         objects = Duration.objects.filter(id__in=data)
#         for d in objects:
#             if d.seconds == 0:
#                 found = True
#                 break
#         if not found:
#             raise ValidationError("Storage durations 0 Minutes required (Baseline)")
#         return data
#
#     def get_subjects_queryset(self):
#         return Subject.objects.filter(owner=self.owner)
#
#     # -------------------Botcatcher-------------------------------------
#     def clean_feedback(self):
#         feedback = self.cleaned_data["feedback"]
#         if len(feedback) > 0:
#             raise forms.ValidationError("We don´t serve your kind here!")
#         return feedback






# class SettingAdminForm(forms.ModelForm):
#     SAMPLETYPE = (
#         # (None, _("All")),
#         (1, _("Venous Blood")),
#         (2, _("Capillary Blood")),
#         (3, _("Arterial Blood")),
#         (4, _("Urine")),
#         (5, _("CSF")),
#         (6, _("Stool")),
#         (7, _("Other - Please specify")),
#     )
#
#     STORAGE = (
#         (1, _("Whole Blood")),
#         (2, _("Plasma/Serum")),
#     )
#
#     CONTAINERADDITIVE = (
#         (0, _("No additive")),
#         (1, _("EDTA")),
#         (2, _("Heparin")),
#         (3, _("Citrate")),
#         (4, _("Clotactivator (Serum)")),
#         (5, _("Other - Please specify")),
#     )
#
#     GEL = (
#         (0, 'False'),
#         (1, 'True'),
#     )
#
#     TYPE = (
#         (1, _("Patients")),
#         (2, _("Healthy volunteers")),
#         (3, _("Other")),
#     )
#
#     DESIGN_SAMPLE = (
#         (1, _("primary samples")),
#         (2, _("aliquots")),
#     )
#
#     TEMPERATURE = (
#         (1, _("Roomtemperature (20 to 25°C)")),
#         (2, _("Refrigerated (2 to 6°C)")),
#         (3, _("Frozen (-15 to -25°C)")),
#         (4, _("Deepfrozen (-60 to -80°C)")),
#         (5, _("Other - Please specify")),
#
#     )
#
#     setting__parameter__parameter__name = forms.ModelChoiceField(
#         queryset=Parameter.objects.all(),
#         label="Select Parameter"
#     )
#     setting__parameter__instrument__manufacturer = forms.CharField(
#         field_name="setting__parameter__instrument__manufacturer",
#         lookup_expr='icontains',
#         label="Analytical Instrument Manufacturer Name contains"
#     )
#     setting__parameter__instrument__name = forms.CharField(
#         field_name="setting__parameter__instrument__name",
#         lookup_expr='icontains',
#         label="Analytical Instrument Name contains"
#     )
#     setting__sample__sample_type = forms.TypedMultipleChoiceField(
#         field_name="setting__sample__sample_type",
#         choices=SAMPLETYPE,
#         widget=forms.CheckboxSelectMultiple,
#         label="Sample type / Matrix"
#     )
#     setting__sample__storage = forms.TypedMultipleChoiceField(
#         field_name="setting__sample__storage",
#         choices=STORAGE,
#         widget=forms.CheckboxSelectMultiple,
#         label="Samples stored as"
#     )
#     setting__sample__container_additive = forms.TypedMultipleChoiceField(
#         field_name="setting__sample__container_additive",
#         choices=CONTAINERADDITIVE,
#         widget=forms.CheckboxSelectMultiple,
#         label="Collection tube additive"
#     )
#     setting__sample__gel = forms.TypedMultipleChoiceField(
#         field_name="setting__sample__gel",
#         choices=GEL,
#         widget=forms.CheckboxSelectMultiple,
#         label="Storage in Sample with gel?"
#     )
#     setting__condition__temperature = forms.TypedMultipleChoiceField(
#         field_name="setting__condition__temperature",
#         choices=TEMPERATURE,
#         widget=forms.CheckboxSelectMultiple,
#         label="Storage temperature"
#     )
#     setting__condition__other_condition = forms.CharField(
#         field_name="setting__condition__other_condition",
#         lookup_expr='icontains',
#         label="Other storage condition contains"
#     )
#     setting__parameter__reagent_name = forms.CharField(
#         field_name="setting__parameter__reagent_name",
#         lookup_expr='icontains',
#         label="Assay Name contains"
#     )
#     setting__parameter__reagent_manufacturer = forms.CharField(
#         field_name="setting__parameter__reagent_manufacturer",
#         lookup_expr='icontains',
#         label="Assay Manufacturer contains"
#     )
#     setting__parameter__analytical_method = forms.CharField(
#         field_name="setting__parameter__analytical_method",
#         lookup_expr='icontains',
#         label="Analytical Method contains"
#     )
#     setting__sample_type = forms.TypedMultipleChoiceField(
#         field_name="setting__sample_type",
#         choices=TYPE,
#         widget=forms.CheckboxSelectMultiple,
#         label="Type of study subjects"
#     )
#     setting__design_sample = forms.TypedMultipleChoiceField(
#         field_name="setting__design_sample",
#         choices=DESIGN_SAMPLE,
#         widget=forms.CheckboxSelectMultiple,
#         label="Samples stored in"
#     )
#
#     class Meta:
#         model = Result
#         fields = [
#
#             'setting__parameter__parameter__name',
#             "setting__parameter__instrument__manufacturer",
#             "setting__parameter__instrument__name",
#             'setting__sample__sample_type',
#             'setting__sample__storage',
#             'setting__sample__container_additive',
#             'setting__sample__gel',
#             'setting__condition__temperature',
#             'setting__condition__other_condition',
#             'setting__parameter__reagent_name',
#             'setting__parameter__reagent_manufacturer',
#             'setting__parameter__analytical_method',
#             'setting__sample_type',
#             'setting__design_sample',
#
#         ]
#     # name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))







#     parameter = forms.ModelChoiceField(queryset=ParameterUser.objects.all(), empty_label='---Select parameter---')
#     sample = forms.ModelChoiceField(queryset=Sample.objects.all(), empty_label='---Select sample---')
#     # durations = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)
#     sample_type = forms.Select()
#     # freeze_thaw = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
#     # design_type = forms.Select()
#     design_sample = forms.Select()
#     # replicate_count = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)
#     condition = forms.ModelChoiceField(queryset=Condition.objects.all(), empty_label='---Select storage condition---')
#     # protocol = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
#     # comment = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
#
#     # owner = None
#     # ----------------------Botcatcher-------------------------
#
#     feedback = forms.CharField(
#         widget=forms.HiddenInput,
#         required=False,
#         validators=[validators.MaxLengthValidator(0)],
#     )
#     # -----------------------------------------------------------
#
#     class Meta:
#         model = Setting
#         fields = (
#             'name',
#             'parameter',
#             'sample',
#             'sample_type',
#             # 'freeze_thaw',
#             'condition',
#             # 'durations',
#             # 'subjects',
#             # 'design_type',
#             'design_sample',
#             # 'protocol',
#             # 'comment',
#             # "replicate_count"
#         )
#
#     def __init__(self, *args, **kwargs):
#         # user = kwargs.pop('user')   #get the correct user for the dropdown-selections
#         # self.owner = user  # retrieve the current user, so that the dropdown of foreignkeys only shows the users own objects
#
#         super().__init__(*args, **kwargs)
#
#         # self.fields['durations'].queryset = Duration.objects.filter(owner=user)
#         # self.fields['durations'].widget = forms.CheckboxSelectMultiple
#         self.fields['subjects'] = forms.ModelMultipleChoiceField(
#             # queryset=Subject.objects.filter(owner=user),
#             widget=forms.CheckboxSelectMultiple,
#         )
#         self.fields['sample'] = forms.ModelChoiceField(
#             # queryset=Sample.objects.filter(owner=user),
#             widget=forms.Select,
#         )
#         self.fields['parameter'].widget.attrs['class'] = 'form-select'
#         self.fields['condition'].widget.attrs['class'] = 'form-select'
#         self.fields['sample'].widget.attrs['class'] = 'form-select'
#         self.fields['sample_type'].widget.attrs['class'] = 'form-select'
#         self.fields['design_sample'].widget.attrs['class'] = 'form-select'
#         self.fields['design_type'].widget.attrs['class'] = 'form-select'
#         # self.fields['sample'].widget.attrs['class'] = 'form-select'
#
#
#     # -------------------Botcatcher-------------------------------------
#     def clean_feedback(self):
#         feedback = self.cleaned_data["feedback"]
#         if len(feedback) > 0:
#             raise forms.ValidationError("We don´t serve your kind here!")
#         return feedback