from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django import forms
from django.urls import reverse
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _


# Create your models here.

class LabUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, help_text='Only used in case we need to get back to you', verbose_name='E-Mail')
    laboratory = models.CharField(_('Name of Laboratory'), max_length=255)
    country = CountryField(verbose_name='Country')
    city = models.CharField(max_length=255, verbose_name='City')
    REQUIRED_FIELDS = ['email', 'laboratory', 'country', 'city']


class Instrument(models.Model):
    author = models.ForeignKey(LabUser, on_delete=models.CASCADE, related_name="todolist", null=True)
    name = models.CharField(max_length=255, verbose_name='Analyzer name', blank=True, null=True)
    manufacturer = models.CharField(max_length=255, verbose_name='Analyzer manufacturer', blank=True, null=True)

    def __str__(self):
        return str('%s %s' % (self.name, self.manufacturer))

    def get_absolute_url(self):
        return reverse('dashboard')

class Condition(models.Model):
    ROOMTEMP = 1
    FRIDGE = 2
    FREEZE = 3
    DEEPFREEZE = 4
    OTHER = 9
    TEMPERATURE = (
        (ROOMTEMP, _("Roomtemperature (20 to 25°C)")),
        (FRIDGE, _("Refrigerated (2 to 6°C)")),
        (FREEZE, _("Frozen (-15 to -25°C")),
        (DEEPFREEZE, _("Deepfrozen (-60 to -80°C)")),
        (OTHER, _("Other - Please specify")),

    )

    temperature = models.SmallIntegerField(
        choices=TEMPERATURE,
        default=FRIDGE,
        verbose_name='Temperature'
    )

    light = models.BooleanField(verbose_name='Exposure to light during storage')
    air = models.BooleanField(verbose_name='Exposure to air during storage')
    agitation = models.BooleanField(verbose_name='Agitation during storage')
    other_Condition=models.CharField(max_length=255, null=True, blank=True, verbose_name='Other Condition')

    # def __str__(self):
    #     return self.temperature

class Sample(models.Model):
    VENOUS_BLOOD = 1
    URINE = 2
    CAPILLARY_BLOOD = 3
    CSF = 4
    STOOL = 5
    ARTERIAL_BLOOD = 6
    OTHER = 9
    SAMPLETYPE = (
        (VENOUS_BLOOD, _("Venous Blood")),
        (URINE, _("Urine")),
        (CAPILLARY_BLOOD, _("Capillary Blood")),
        (CSF, _("CSF")),
        (STOOL, _("Stool")),
        (ARTERIAL_BLOOD, _("Arterial Blood")),
        (OTHER, _("Other - Please specify")),

    )

    sample_type = models.SmallIntegerField(
        choices=SAMPLETYPE,
        default=VENOUS_BLOOD,
        verbose_name='Sample Type'
    )

    PLASTIC = 1
    GLASS = 2
    OTHER = 3
    CONTAINERMATERIAL = (
        (PLASTIC, _("Plastic")),
        (GLASS, _("Glass")),
        (OTHER, _("Other - Please specify")),
    )

    container_material = models.SmallIntegerField(
        choices=CONTAINERMATERIAL,
        default=PLASTIC,
        verbose_name='Container Material'
    )

    SMALL = 1
    MIDDLE = 2
    BIG = 3
    OTHER = 4
    CONTAINERDIMENSION = (
        (SMALL, _("13x75mm")),
        (MIDDLE, _("13x100mm")),
        (BIG, _("16x100mm")),
        (OTHER, _("Other - Please specify")),
    )

    container_dimension = models.SmallIntegerField(
        choices=CONTAINERDIMENSION,
        default=SMALL,
        verbose_name='Container Dimension'
        , blank=True, null=True
    )

    container_fillingvolume = models.FloatField(verbose_name='Container Fillingvolume', blank=True, null=True)

    NONE = 0
    EDTA = 1
    HEP = 2
    CITRATE = 3
    CLOTACTIVATOR = 6
    Other = 9
    CONTAINERADDITIVE = (
        (NONE, _("No additive")),
        (EDTA, _("EDTA")),
        (HEP, _("Heparin")),
        (CITRATE, _("Citrate")),
        (CLOTACTIVATOR, _("Clotactivator (Serum)")),
        (OTHER, _("Other - Please specify")),

    )

    container_additive = models.SmallIntegerField(
        choices=CONTAINERADDITIVE,
        # default=HOURS,
        verbose_name='Container Additive', blank=True, null=True
    )

    gel = models.BooleanField(verbose_name='Container with gel', blank=True, null=True)

    # def __str__(self):
    #     return self.sample_type
    def __str__(self):
        return str('%s %s' % (self.sample_type, self.container_additive))
    # TODO: Show name of choices rather than numbers


class Parameter(models.Model):
    name = models.CharField(max_length=255, verbose_name='Parameter Name')
    unit = models.CharField(max_length=15, verbose_name='Parameter Unit')
    reagent_name = models.CharField(max_length=255, verbose_name='Reagent name', blank=True, null=True)
    reagent_manufacturer = models.CharField(max_length=255, verbose_name='Reagent manufacturer', blank=True, null=True)
    CV_intra = models.FloatField(verbose_name='CV% intra', blank=True, null=True)
    CV_inter = models.FloatField(verbose_name='CV% inter', blank=True, null=True)
    method_hand = models.BooleanField(verbose_name='Manual method', blank=True, null=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, blank=True, null=True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Value(models.Model):
    value = models.FloatField()
    duration = models.ForeignKey("Duration", on_delete=models.CASCADE, related_name='value_set')

class Duration(models.Model):
    # DURATION_CHOICES = [(x, x) for x in range(1, 32)]
    #
    # duration_number = forms.ChoiceField(choices=DURATION_CHOICES)

    duration_number = models.IntegerField(choices=list(zip(range(1, 32), range(1, 32))), unique=True)

    MINUTES = "MIN"
    HOURS = "HR"
    DAYS = "DAY"
    MONTHS = "MON"
    YEARS = "YEAR"
    DURATION = (
        (MINUTES, _("Minute(s)")),
        (HOURS, _("Hour(s)")),
        (DAYS, _("Day(s)")),
        (MONTHS, _("Month(s)")),
        (YEARS, _("Year(s)")),

    )

    duration_unit = models.CharField(
        max_length=4,
        choices=DURATION,
        default=HOURS,
    )
    value = models.ForeignKey(Value, on_delete=models.CASCADE, related_name='duration_value_set')
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE, related_name='duration_subject_set')
    def __str__(self):
        return str('%s %s' % (self.duration_number, self.duration_unit))


class Subject(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    duration = models.ForeignKey(Duration, on_delete=models.CASCADE, related_name='subject_duration_set')
    setting = models.ForeignKey('Setting', on_delete=models.CASCADE, related_name='subject_setting_set')
    def __str__(self):
        return self.name

# class Population(models.Model):
#     title = models.CharField(max_length=255, verbose_name="Population Title")
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE, help_text='How many patients/volunteers were recruited?')
#     replicates = models.SmallIntegerField(help_text='How many replicate measurements did you perform per sample?', choices=list(zip(range(1, 11), range(1, 11))))
#
#     def __str__(self):
#         return self.title

class Setting(models.Model):
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
    # population = models.ForeignKey(Population, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='setting_set')


