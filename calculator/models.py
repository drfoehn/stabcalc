from decimal import Decimal, getcontext

from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django import forms
from django.urls import reverse
from django.utils.functional import cached_property
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
import math
import statistics


# Create your models here.

class LabUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, help_text='Only used in case we need to get back to you',
                              verbose_name='E-Mail')
    laboratory = models.CharField(_('Name of Laboratory'), max_length=255)
    country = CountryField(verbose_name='Country')
    city = models.CharField(max_length=255, verbose_name='City')
    REQUIRED_FIELDS = ['email', 'laboratory', 'country', 'city']


class Instrument(models.Model):
    author = models.ForeignKey(LabUser, on_delete=models.CASCADE, related_name="todolist", null=True)
    name = models.CharField(max_length=255, verbose_name='Analyzer name', blank=True, null=True)
    manufacturer = models.CharField(max_length=255, verbose_name='Analyzer manufacturer', blank=True, null=True)

    def __str__(self):
        return f"{self.name}, {self.manufacturer}"

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
    other_Condition = models.CharField(max_length=255, null=True, blank=True, verbose_name='Other Condition')

    def __str__(self):
        return f"{self.get_temperature_display()}, Light: {self.light}, Air: {self.air}, Agitation: {self.agitation}, Other: {self.other_Condition}"


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
        return f"{self.get_sample_type_display()} - {self.container_fillingvolume}ml {self.get_container_additive_display()} ({self.get_container_dimension_display()}, {self.get_container_material_display()}); Gel: {self.gel}"


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
        return f"{self.name} - Intrument: {self.instrument.name} / Handmethod: {self.method_hand}"


class Setting(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True,
                            help_text='Choose any name that identifies your stability study')
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, blank=True, null=True)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE, blank=True, null=True)
    replicates = models.SmallIntegerField(help_text='How many replicate measurements did you perform per sample?',
                                          choices=list(zip(range(1, 11), range(1, 11))))

    def __str__(self):
        return f"{self.name} ({self.parameter.name} / {self.condition.get_temperature_display()} / Other condition: {self.condition.other_Condition} / Replicates: {self.replicates}) "

    def values_tot(self, duration: 'Duration'):
        return [v.value for v in Result.objects.filter(setting=self, duration=duration)]

    def average_tot(self, duration: 'Duration'):
        values = self.values_tot(duration)
        if not values:
            return "-"
        else:
            return math.ceil((statistics.mean(values))*100)/100


class Duration(models.Model):
    class Meta:
        unique_together = ["duration_number", "duration_unit"]
        ordering = ["seconds"]

    duration_number = models.PositiveIntegerField(blank=True, null=True)

    MINUTES = "1"
    HOURS = "2"
    DAYS = "3"
    MONTHS = "4"
    YEARS = "5"
    DurationChoices = (
        (MINUTES, _("Minute(s)")),
        (HOURS, _("Hour(s)")),
        (DAYS, _("Day(s)")),
        (MONTHS, _("Month(s)")),
        (YEARS, _("Year(s)")),
    )
    duration_unit = models.CharField(
        choices=DurationChoices,
        blank=True, null=True,
        max_length=1
    )

    setting = models.ManyToManyField(Setting)

    seconds = models.PositiveIntegerField(blank=True)

    def save(
            self, *args, **kwargs
    ):
        calc_tbl = {
            self.MINUTES: 60,
            self.HOURS: 60 * 60,
            self.DAYS: 60 * 60 * 24,
            self.MONTHS: 60 * 60 * 24 * 30,
            self.YEARS: 60 * 60 * 24 * 365,
        }
        self.seconds = calc_tbl[self.duration_unit] * self.duration_number
        super().save(*args, **kwargs)

    def __str__(self):
        unit = self.get_duration_unit_display()
        return f"{self.duration_number}, {unit}"

    def replicates(self):
        return self.setting.replicates



class Subject(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    def values(self, duration: Duration):
        return [v.value for v in Result.objects.filter(replicate__in=self.replicate_set.all(), duration=duration)]



    def average(self, duration: Duration):
        values = self.values(duration)
        if not values:
            return "-"
        else:
            return math.ceil((statistics.mean(values))*100)/100

    def stdv(self, duration: Duration):
        values = self.values(duration)
        if len(values) < 2:
            return "-"
        else:
            return math.ceil((statistics.stdev(values))*100)/100

    def cv(self, duration: Duration):

        average = self.average(duration)
        stdv = self.stdv(duration)

        if average == '-':
            return '-'
        elif stdv == '-':
            return '-'
        else:
            return math.ceil(((stdv / average) * 100)*100)/100



# TODO: Funktion funzt nicht - Alternativ derzeit .count im templatetag
    # def number_of_subjects(self, setting: Setting):
    #     nr = self.objects.count(setting)
    #     if not nr:
    #         return "-"
    #     else:
    #         return nr


class Replicate(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    # result_set

    # TODO: Pro Replicate darf nur eine Duration eingegeben werden

    def __str__(self):
        return str(self.id)  # FIXME: Zahl des Replicates ausgeben


class Result(models.Model):
    value = models.FloatField()
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE)
    replicate = models.ForeignKey(Replicate, on_delete=models.CASCADE)
    duration = models.ForeignKey(Duration, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    # def subject(self):
    #     return self.replicate.subject

    def __str__(self):
        return str(self.value)

    # def duration(self):
    #     return self.subject.duration

    # def average(self):
    #     results = self.objects.all()
    #     SumOfResults = sum(results)
    #     count = len(results)
    #     average = SumOfResults/count
    #     print("Entered results: ", results)
    #     print("Average: ", average)
