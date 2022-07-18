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
from users.models import LabUser


class OwnedModelMixin(models.Model):
    owner = models.ForeignKey(LabUser, on_delete=models.PROTECT)

    class Meta:
        abstract = True


class Instrument(OwnedModelMixin, models.Model):
    name = models.CharField(max_length=255, verbose_name='Analyzer name', blank=True, null=True)
    manufacturer = models.CharField(max_length=255, verbose_name='Analyzer manufacturer', blank=True, null=True)

    def __str__(self):
        return f"{self.name}, {self.manufacturer}"

class Condition(OwnedModelMixin, models.Model):
    ROOMTEMP = 1
    FRIDGE = 2
    FREEZE = 3
    DEEPFREEZE = 4
    OTHER = 9
    TEMPERATURE = (
        (ROOMTEMP, _("Roomtemperature (20 to 25°C)")),
        (FRIDGE, _("Refrigerated (2 to 6°C)")),
        (FREEZE, _("Frozen (-15 to -25°C)")),
        (DEEPFREEZE, _("Deepfrozen (-60 to -80°C)")),
        (OTHER, _("Other - Please specify")),

    )

    temperature = models.SmallIntegerField(
        choices=TEMPERATURE,
        default=FRIDGE,
        verbose_name='Temperature'
    )
    temperature_other = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Other Temperature'))
    thawing = models.CharField(max_length=400, verbose_name=_('How were frozen samples thawed?'), blank=True, null=True)
    temperature_monitor = models.CharField(max_length=255, verbose_name=_('How was the storage temperature monitored?'))

    # CHOICES_BOOLEAN = (
    #     (True, _('Yes')),
    #     (False, _('No'))
    # )
    light = models.BooleanField(verbose_name=_('Exposure to light during storage'))
    air = models.BooleanField(verbose_name=_('Contact to air during storage'))
    cell = models.BooleanField(verbose_name=_('Contact to cells during storage?'))
    agitation = models.BooleanField(verbose_name=_('Agitation during storage'))
    other_condition = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Other Condition'))

    def __str__(self):
        return f"{self.get_temperature_display()}, Light: {self.light}, Air: {self.air}, Agitation: {self.agitation}, Other: {self.other_condition}"

class PreanalyticalSet(OwnedModelMixin, models.Model):
    collection_instrument = models.CharField(max_length=255, verbose_name=_('Sample collection set'), blank=True, null=True)
    collection_site = models.CharField(max_length=255, verbose_name=_('Sample collection site'))
    transportation_temp = models.SmallIntegerField(verbose_name=_('Transportation temperature'))

    PTS = 1
    CARRIER = 2
    TRAIN = 3
    PLANE = 4
    CAR = 5
    OTHER = 9
    TRANSPORTATION = (
        (PTS, _("Pneumatic tube system")),
        (CARRIER, _("manual - by Carrier")),
        (TRAIN, _("by Train")),
        (PLANE, _("by Plane")),
        (CAR, _("by Car")),
        (OTHER, _("Other - Please specify")),

    )

    transportation_method = models.SmallIntegerField(
        choices=TRANSPORTATION,
        verbose_name='Transportation method'
    )
    transportation_method_other = models.CharField(max_length=255, verbose_name=_('Other'), blank=True, null=True)

    MINUTES = "1"
    HOURS = "2"
    DAYS = "3"
    DurationChoices = (
        (MINUTES, _("Minute(s)")),
        (HOURS, _("Hour(s)")),
        (DAYS, _("Day(s)")),
    )
    transportation_time_unit = models.CharField(
        choices=DurationChoices,
        max_length=1
    )
    transportation_time = models.PositiveIntegerField(verbose_name=_('Time from sample collection to separation'))
    centrifugation_g = models.SmallIntegerField(verbose_name=_('Centrifugation speed (*g)'), blank=True, null=True)
    centrifugation_time = models.SmallIntegerField(verbose_name=_('Centrifugation time (min)'), blank=True, null=True)
    centrifugation_temp = models.SmallIntegerField(verbose_name=_('Centrifugation temperature (°C)'), blank=True, null=True)
    comment = models.TextField(verbose_name=_('Preanalytical comment'), blank=True, null=True)

    def __str__(self):
        return f"{self.collection_site}"

class Sample(OwnedModelMixin, models.Model):
    sample_leftover = models.BooleanField(verbose_name=_('Were the used samples leftovers from routine processes?'), blank=True, null=True)
    sample_pool = models.BooleanField(verbose_name=_('Were the used samples pooled samples?'), blank=True, null=True)
    sample_pool_text = models.TextField(verbose_name=_('How and form what samples were study samples pooled?'), blank=True, null=True)
    sample_spike = models.BooleanField(verbose_name=_('Were analytes spiked in study samples?'), blank=True, null=True)
    sample_spike_text = models.TextField(verbose_name=_('Which analytes were spiked and how?'), blank=True, null=True)

    VENOUS_BLOOD = 1
    CAPILLARY_BLOOD = 2
    ARTERIAL_BLOOD = 3
    URINE = 4
    CSF = 5
    STOOL = 6
    OTHER = 9
    SAMPLETYPE = (
        (VENOUS_BLOOD, _("Venous Blood")),
        (CAPILLARY_BLOOD, _("Capillary Blood")),
        (ARTERIAL_BLOOD, _("Arterial Blood")),
        (URINE, _("Urine")),
        (CSF, _("CSF")),
        (STOOL, _("Stool")),
        (OTHER, _("Other - Please specify")),

    )

    sample_type = models.SmallIntegerField(
        choices=SAMPLETYPE,
        default=VENOUS_BLOOD,
        verbose_name='Sample Type'
    )
    sample_type_other = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Other Sampletype'))

    WHOLEBLOOD = 1
    PLASMA = 2
    STORAGE = (
        (WHOLEBLOOD, _("Whole Blood")),
        (PLASMA, _("Plasma/Serum")),
    )

    storage = models.SmallIntegerField(
        choices=STORAGE,
        verbose_name='Blood storage as'
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
    container_material_other = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Other Containermaterial'))

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

    container_dimension_other = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Other Containerdimension'))

    container_fillingvolume = models.FloatField(verbose_name='Container Fillingvolume (in mL)', blank=True, null=True)

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
    container_additive_other = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Other Additive'))
    gel = models.BooleanField(verbose_name='Container with gel', blank=True, null=True)
    preanalytical_set = models.ForeignKey(PreanalyticalSet, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_sample_type_display()} - {self.container_fillingvolume}ml {self.get_container_additive_display()} ({self.get_container_dimension_display()}, {self.get_container_material_display()}); Gel: {self.gel}"


class Parameter(OwnedModelMixin, models.Model):
    name = models.CharField(max_length=255, verbose_name='Parameter Name')
    unit = models.CharField(max_length=15, verbose_name='Parameter Unit')
    reagent_name = models.CharField(max_length=255, verbose_name='Reagent name', blank=True, null=True)
    reagent_manufacturer = models.CharField(max_length=255, verbose_name='Reagent manufacturer', blank=True, null=True)
    analytical_method = models.CharField(max_length=255, verbose_name='Analytical method')
    CV_intra = models.FloatField(verbose_name='CV% intra', blank=True, null=True)
    CV_inter = models.FloatField(verbose_name='CV% inter', blank=True, null=True)
    method_hand = models.BooleanField(verbose_name='Manual method', blank=True, null=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, blank=True, null=True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        permissions = (
            ('dg_view_parameter', 'OLP can view Parameter'),
        )

    def __str__(self):
        return f"{self.name}"


class Setting(OwnedModelMixin, models.Model):
    name = models.CharField(max_length=255, blank=True, null=True,
                            help_text='Choose any name that identifies your stability study')
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, blank=True, null=True)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE, blank=True, null=True)
    #FIXME: rename in subjects
    subject = models.ManyToManyField('Subject', blank=True, related_name='settings')
    duration = models.ManyToManyField('Duration', blank=True)
    sample = models.ForeignKey('Sample', on_delete=models.CASCADE)
    freeze_thaw_cycles = models.SmallIntegerField(verbose_name=_('How many freeze/thaw cycles did the samples endure?'), blank=True, null=True)

    PATIENT = 1
    HEALTHY = 2
    OTHER = 3
    TYPE = (
        (PATIENT, _("Patient samples")),
        (HEALTHY, _("Healthy volunteers")),
        (OTHER, _("Other")),

    )

    sample_type = models.SmallIntegerField(
        choices=TYPE,
        # default=HOURS,
        verbose_name='Type of study subject'
    )


    ISOCHRONUS = 1
    REALTIME = 2
    DESIGN_TYPE = (
        (ISOCHRONUS, _("Isochronus")),
        (REALTIME, _("Real time")),

    )

    design_type = models.SmallIntegerField(
        choices=DESIGN_TYPE,
        verbose_name='Type of study design'
    )

    PRIMARY = 1
    ALIQUOT = 2
    DESIGN_SAMPLE = (
        (PRIMARY, _("primary samples")),
        (ALIQUOT, _("aliquots")),

    )

    design_sample = models.SmallIntegerField(
        choices=DESIGN_SAMPLE,
        verbose_name='Type of study design'
    )

    protocol = models.TextField(verbose_name=_('Study protocol'), blank=True, null=True)
    comment = models.CharField(max_length=1000, blank=True, null=True, help_text='Insert all additional information to the setting here')

    def __str__(self):
        return f"{self.name}: {self.parameter.name} / {self.condition.get_temperature_display()} / Other condition: {self.condition.other_condition}"

    def values_tot(self, duration: 'Duration') -> list[float]:
        return [v.value for v in Result.objects.filter(setting=self, duration=duration)]

    def average_tot(self, duration: 'Duration') -> float | None:
        values = self.values_tot(duration)
        if not values:
            return None
        else:
            return math.ceil((statistics.mean(values)) * 100) / 100

    def stdv_tot(self, duration: 'Duration') -> float | None:
        values = self.values_tot(duration)
        if len(values) < 2:
            return None
        else:
            return math.ceil((statistics.stdev(values)) * 100) / 100

    def avg_tot_sd_h(self, duration: 'Duration') -> float | None:
        values = self.values_tot(duration)
        if len(values) < 2:
            return None
        else:
            return math.ceil((statistics.mean(values) + statistics.stdev(values)) * 100) / 100

    def avg_tot_sd_l(self, duration: 'Duration') -> float | None:
        values = self.values_tot(duration)
        if len(values) < 2:
            return None
        else:
            return math.ceil((statistics.mean(values) - statistics.stdev(values)) * 100) / 100

    def cv_tot(self, duration: 'Duration') -> float | None:
        average = self.average_tot(duration)
        stdv = self.stdv_tot(duration)
        if not average or not stdv:
            return None
        else:
            return math.ceil(((stdv / average) * 100) * 100) / 100

    def cv_max(self) -> float | None:
        analytical_cv = self.parameter.CV_intra
        if not analytical_cv:
            return None
        else:
            return round(analytical_cv*3, 2)

    def cv_max_abs_high(self, duration: 'Duration') -> float | None:
        analytical_cv = self.parameter.CV_intra
        average_tot= self.average_tot(duration)
        if not analytical_cv:
            return None
        else:
            return  average_tot*(((analytical_cv*3)+1)/100)+average_tot

    def cv_max_abs_low(self, duration: 'Duration') -> float | None:
        analytical_cv = self.parameter.CV_intra
        average_tot= self.average_tot(duration)
        if not analytical_cv:
            return None
        else:
            return  average_tot-average_tot*(((analytical_cv*3)+1)/100)

    def deviation_tot(self, duration: 'Duration') -> float | None:
        average = self.average_tot(duration)
        duration_zero = Duration.objects.get(duration_number=0)
        average_zero = self.average_tot(duration_zero)
        if not average or not average_zero:
            return None
        else:
            return math.ceil((((average - average_zero) / average_zero) * 100) * 100) / 100

    # def save(self, *args, **kwargs):
    #     dur_zero = Duration.objects.create(duration_number=0, duration_unit="1")
    #     # TODO: add if not
    #     self.duration_set.add(dur_zero)
    #     super().save(*args, **kwargs)


class Duration(OwnedModelMixin, models.Model):
    class Meta:
        # unique_together = ["duration_number", "duration_unit"]
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

    def converted_time(self):
        minutes = self.seconds/60
        hours = self.seconds/3600
        days = self.seconds/3600/24
        months = self.seconds/3600/24/30
        years = self.seconds/3600/24/365

        if years >= 1:
            return str(years) + ' years, ' + str(months) + ' months, ' + str(days) + ' days'
        elif months >= 1 and years <1:
            return str(months) + ' months, ' + str(days) + ' days'
        elif days >= 1 and months <1:
            return str(days) + ' days' + str(hours) + ' hours'
        elif hours >=1 and days <1:
            return str(hours) + ' hours'


    def __str__(self):
        unit = self.get_duration_unit_display()
        return f"{self.duration_number}, {unit}"


# duration, created = Duration.objects.get_or_create(
#         seconds=0,
#         defaults={'duration_number': 0, 'duration_unit': '1'},
#     )

#FIXME: This calls the duration table upon makemigrations, which does not exist at that time.


class Subject(OwnedModelMixin, models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

    def _results(self, duration: Duration, setting: Setting):
        return [v.value for v in
                Result.objects.filter(duration=duration, subject=self, setting=setting)]

    def average(self, duration: Duration, setting: Setting) -> float|None:
        values = self._results(duration, setting)
        if not values:
            return None
        else:
            return math.ceil((statistics.mean(values)) * 100) / 100

    def stdv(self, duration: Duration, setting: Setting) -> float|None:
        values = self._results(duration, setting)
        if len(values) < 2:
            return None
        else:
            return math.ceil((statistics.stdev(values)) * 100) / 100

    def cv(self, duration: Duration, setting: Setting) -> float|None:

        average = self.average(duration, setting)
        stdv = self.stdv(duration, setting)

        if not average or not stdv:
            return None
        else:
            return math.ceil(((stdv / average) * 100) * 100) / 100

    def deviation(self, duration: Duration, setting: Setting) -> float|None:
        average = self.average(duration, setting)
        duration_zero = Duration.objects.get(duration_number=0)
        average_zero = self.average(duration_zero, setting)
        if not average or not average_zero:
            return None
        else:
            return math.ceil((((average - average_zero) / average_zero) * 100) * 100) / 100

class Result(OwnedModelMixin, models.Model):
    value = models.FloatField()
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE, blank=True)
    duration = models.ForeignKey(Duration, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    # def duration_cat(self):
    #     return str(self.duration.duration_number) + self.duration.get_duration_unit_display()

    def __str__(self):
        return f"{self.value}, {self.duration}, {self.subject.name}, {self.setting_id}, {self.id}"

    # def duration(self):
    #     return self.subject.duration

    # def average(self):
    #     results = self.objects.all()
    #     SumOfResults = sum(results)
    #     count = len(results)
    #     average = SumOfResults/count
    #     print("Entered results: ", results)
    #     print("Average: ", average)


# TODO: Funktion funzt nicht - Alternativ derzeit .count im templatetag
# def number_of_subjects(self, setting: Setting):
#     nr = self.objects.count(setting)
#     if not nr:
#         return "-"
#     else:
#         return nr


