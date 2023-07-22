from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Literature(models.Model):
    lit_id = models.AutoField(primary_key=True)
    lit_no = models.CharField(max_length=5)
    # analyte_id = models.CharField(max_length=255, blank=True, null=True)
    authors = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    doi = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.lit_no}, {self.title}"

    class Meta:
        verbose_name = "Literature"
        verbose_name_plural = "Literature"

class Platform(models.Model):
    pt_id = models.AutoField(primary_key=True)
    pt_id_orig = models.IntegerField(blank=True, null=True)
    flag = models.CharField(max_length=3, blank=True, null=True)
    set_value = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    instrument = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.company}; {self.instrument}"

    class Meta:
        verbose_name = "Platform"
        verbose_name_plural = "Platforms"


# class StabilitySampleGroup(models.Model):
#     stabgroup_id = models.AutoField(primary_key=True)
#     abbr = models.CharField(max_length=255, blank=True, null=True)
#     name = models.CharField(max_length=255, blank=True, null=True)
#
#     def __str__(self):
#         return self.name
class Specimen(models.Model):
    sg_id = models.AutoField(primary_key=True)
    abbr = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
class SampleType(models.Model):
    sat_id = models.AutoField(primary_key=True)
    abbr = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return f"{self.name}"

class AnalytMethod(models.Model):
    meth_id = models.AutoField(primary_key=True)
    abbr = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Unit(models.Model):
    unit_id = models.AutoField(primary_key=True)
    abbr = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    SI = "1"
    KO = "2"
    UnitChoices = (
        (SI, _("S.I.")),
        (KO, _("Convetional")),
    )
    unit_type = models.CharField(
        choices=UnitChoices,
        blank=True, null=True,
        max_length=1
    )

    def __str__(self):
        return self.name

class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    abbr = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Stability(models.Model):

    stab_id = models.AutoField(primary_key=True)

    LIN = "1"
    QUADR = "2"
    CUBIC = "3"
    EXP = "4"

    EQTypeChoices = (
        (LIN, _("Linear (1°)")),
        (QUADR, _("Quadratic (2°)")),
        (CUBIC, _("Cubic (3°)")),
        (EXP, _("Exponential")),
    )

    RT = "1"
    REFRIG = "2"
    FROZEN = "3"
    DEEPFROZEN = "4"
    ULTRADEEPFROZEN = "5"

    TemepratureChoices = (
        (RT, _("Room Temperature (20 to 25°C)")),
        (REFRIG, _("Refrigerated (2 to 8°C)")),
        (FROZEN, _("Frozen (-15 to -25°C)")),
        (DEEPFROZEN, _("Deepfrozen (-60 to -80°C)")),
        (ULTRADEEPFROZEN, _("Ultradeepfrozen( < -80°C)")),
    )
    temperature = models.CharField(choices=TemepratureChoices, blank=True, null=True, max_length=1)


    abs_min_prefix = models.CharField(max_length=5, blank=True, null=True)
    abs_min = models.FloatField(blank=True, null=True)
    abs_max_prefix = models.CharField(max_length=5, blank=True, null=True)
    abs_max = models.FloatField(blank=True, null=True)
    eq_type = models.CharField(choices=EQTypeChoices,blank=True, null=True, max_length=1)
    b0 = models.FloatField(blank=True, null=True, help_text="If forced through zero, B0 has to be 0")
    b1 = models.FloatField(blank=True, null=True)
    b2 = models.FloatField(blank=True, null=True)
    b3 = models.FloatField(blank=True, null=True)
    exp_a = models.FloatField(blank=True, null=True)
    exp_b = models.FloatField(blank=True, null=True)
    orig_import = models.CharField(max_length=255, blank=True, null=True)
    stabilizer = models.CharField(max_length=255, blank=True, null=True)
    stab_platform = models.ForeignKey(Platform, on_delete=models.CASCADE, blank=True, null=True)
    stab_analyt_method = models.ForeignKey(AnalytMethod, on_delete=models.CASCADE, blank=True, null=True)
    stab_literature = models.ManyToManyField(Literature)
    stab_comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_temperature_display()} - {self.stab_id}"

    class Meta:
        verbose_name = "Stability"
        verbose_name_plural = "Stabilities"

class Analyte(models.Model):
    aid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    abbr = models.CharField(max_length=255, blank=True, null=True)
    details = models.CharField(max_length=255, blank=True, null=True)
    specimen = models.ManyToManyField(Specimen, through='AnalyteSpecimen')
    category = models.ManyToManyField(Category)
    bhl_min = models.FloatField(blank=True, null=True)
    bhl_max = models.FloatField(blank=True, null=True)
    bhl_comment = models.CharField(max_length=255, blank=True, null=True)
    bhl_literature = models.ManyToManyField(Literature, related_name='bhl_literature')

    def __str__(self):
        return f"{self.name}, {self.details}"

class AnalyteSpecimen(models.Model):
    analyte = models.ForeignKey(Analyte, related_name="analyte_specimen", on_delete=models.CASCADE)
    specimen = models.ForeignKey(Specimen, related_name="specimen_analyte", on_delete=models.CASCADE)
    unit = models.ManyToManyField(Unit)
    stability = models.ManyToManyField(Stability, blank=True)
    annotation = models.CharField(max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    tube_not = models.ManyToManyField(SampleType, blank=True, related_name='tube_not_sampletype')
    tube_maybeposs = models.ManyToManyField(SampleType, blank=True, related_name='tube_maybe_sampletype')
    tube_possible = models.ManyToManyField(SampleType, blank=True, related_name='tube_possible_sampletype')
    tube_recomm = models.ManyToManyField(SampleType, blank=True, related_name='tube_recomm_sampletype')
    tube_not_comment = models.CharField(max_length=255, blank=True, null=True)
    tube_maybeposs_comment = models.CharField(max_length=255, blank=True, null=True)
    tube_possible_comment = models.CharField(max_length=255, blank=True, null=True)
    tube_recomm_comment = models.CharField(max_length=255, blank=True, null=True)
    cvi_url = models.URLField(blank=True, null=True)
    loinc_num = models.CharField(max_length=50, blank=True, null=True)
    loinc_component = models.CharField(max_length=255, blank=True, null=True)
    loinc_short_name= models.CharField(max_length=255, blank=True, null=True)
    loinc_long_name= models.CharField(max_length=255, blank=True, null=True)
    loinc_class = models.CharField(max_length=255, blank=True, null=True)
    loinc_url = models.URLField(blank=True, null=True)


    def __str__(self):
        if self.analyte.details:
            return f"{self.analyte.name} - {self.analyte.details} in {self.specimen.name}"
        else:
            return f"{self.analyte.name} in {self.specimen.name}"

    # def get_fields(self):
    #     field_values = []
    #     for field in AnalyteSpecimen._meta.get_fields():
    #         value = getattr(self, field.name)
    #         if field.is_relation:
    #             if field.many_to_many:
    #                 if value.exists():  # Überprüfe, ob es zugehörige Objekte gibt
    #                     field_values.append((field.name, value.all()))
    #             else:  # Es handelt sich um einen FK
    #                 if value is not None:  # Überprüfe, ob es ein zugehöriges Objekt gibt
    #                     field_values.append((field.name, value))
    #         else:  # Es handelt sich um ein normales Feld
    #             if value:
    #                 field_values.append((field.name, value))
    #     return field_values