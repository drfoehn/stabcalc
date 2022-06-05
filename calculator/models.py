from django.db import models
from django import forms
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Instrument(models.Model):
    hand = models.BooleanField(verbose_name='Manual method', blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name='Analyzer name', blank=True, null=True)
    manufacturer = models.CharField(max_length=255, verbose_name='Analyzer manufacturer', blank=True, null=True)


    def __str__(self):
        return self.name

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

    container_fillingvolume = models.FloatField(verbose_name='Container Fillingvolume')

    EDTA = 1
    HEP = 2
    CITRATE = 3
    SERUM = 4
    URINE = 5
    Other = 9
    CONTAINERADDITIVE = (
        (EDTA, _("EDTA")),
        (HEP, _("Heparin")),
        (CITRATE, _("Citrate")),
        (SERUM, _("Serum")),
        (URINE, _("Urine")),
        (OTHER, _("Other - Please specify")),

    )

    container_additive = models.SmallIntegerField(
        choices=CONTAINERADDITIVE,
        # default=HOURS,
        verbose_name='Container Additive', blank=True, null=True
    )

    gel = models.BooleanField(verbose_name='Container with gel')

    # def __str__(self):
    #     return self.sample_type


class Parameter(models.Model):
    name = models.CharField(max_length=255, verbose_name='Parameter Name')
    unit = models.CharField(max_length=15, verbose_name='Parameter Unit')
    reagent_name = models.CharField(max_length=255, verbose_name='Reagent name', blank=True, null=True)
    reagent_manufacturer = models.CharField(max_length=255, verbose_name='Reagent manufacturer', blank=True, null=True)
    CV_intra = models.FloatField(verbose_name='CV% intra', blank=True, null=True)
    CV_inter = models.FloatField(verbose_name='CV% inter', blank=True, null=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Duration(models.Model):
    # DURATION_CHOICES = [(x, x) for x in range(1, 32)]
    #
    # duration_number = forms.ChoiceField(choices=DURATION_CHOICES)

    duration_number =  models.IntegerField(choices=list(zip(range(1, 32), range(1, 32))), unique=True)

    MINUTES = "MIN"
    HOURS = "HR"
    DAYS = "DY"
    MONTHS = "MON"
    YEARS = "YR"
    DURATION = (
        (MINUTES, _("Minute(s)")),
        (HOURS, _("Hour(s)")),
        (DAYS, _("Day(s)")),
        (MONTHS, _("Month(s)")),
        (YEARS, _("Year(s)")),

    )

    duration_unit = models.CharField(
        max_length=3,
        choices=DURATION,
        default=HOURS,
    )

    # def __str__(self):
    #     return self.duration_number


class Result(models.Model):
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
    duration = models.ForeignKey(Duration, on_delete=models.CASCADE)
    value = models.FloatField()

