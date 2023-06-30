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
    doi_url = models.URLField(max_length=255, blank=True, null=True)
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
class SampleGroup(models.Model):
    sg_id = models.AutoField(primary_key=True)
    abbr = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
class SampleType(models.Model):
    sat_id = models.AutoField(primary_key=True)
    abbr = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    group = models.ForeignKey(SampleGroup, on_delete=models.CASCADE, blank=True, null=True)
    # TODO: Add all entries where there is a comment to the tube type - e.g. - "&#8599;"  - from table stability_all_de
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

    stab_id = models.AutoField(primary_key=True)
    analyte_name = models.CharField(max_length=255, blank=True, null=True)
    rt_abs_min_prefix = models.CharField(max_length=5, blank=True, null=True)
    rt_abs_min = models.FloatField(blank=True, null=True)
    rt_abs_max_prefix = models.CharField(max_length=5, blank=True, null=True)
    rt_abs_max = models.FloatField(blank=True, null=True)
    rt_eq_type = models.CharField(choices=EQTypeChoices,blank=True, null=True, max_length=1)
    rt_b0 = models.FloatField(blank=True, null=True, help_text="If forced through zero, B0 has to be 0")
    rt_b1 = models.FloatField(blank=True, null=True)
    rt_b2 = models.FloatField(blank=True, null=True)
    rt_exp_a = models.FloatField(blank=True, null=True)
    rt_exp_b = models.FloatField(blank=True, null=True)
    rt_comment = models.CharField(max_length=255, blank=True, null=True)
    rt_import = models.CharField(max_length=255, blank=True, null=True)
    refrig_abs_min_prefix = models.CharField(max_length=5, blank=True, null=True)
    refrig_abs_min = models.FloatField(blank=True, null=True)
    refrig_abs_max_prefix = models.CharField(max_length=5, blank=True, null=True)
    refrig_abs_max = models.FloatField(blank=True, null=True)
    refrig_eq_type = models.CharField(choices=EQTypeChoices,blank=True, null=True, max_length=1)
    refrig_b0 = models.FloatField(blank=True, null=True, help_text="If forced through zero, B0 has to be 0")
    refrig_b1 = models.FloatField(blank=True, null=True)
    refrig_b2 = models.FloatField(blank=True, null=True)
    refrig_exp_a = models.FloatField(blank=True, null=True)
    refrig_exp_b = models.FloatField(blank=True, null=True)
    refrig_comment = models.CharField(max_length=255, blank=True, null=True)
    refrig_import = models.CharField(max_length=255, blank=True, null=True)
    frozen_abs_min_prefix = models.CharField(max_length=5, blank=True, null=True)
    frozen_abs_min = models.FloatField(blank=True, null=True)
    frozen_abs_max_prefix = models.CharField(max_length=5, blank=True, null=True)
    frozen_abs_max = models.FloatField(blank=True, null=True)
    frozen_eq_type = models.CharField(choices=EQTypeChoices,blank=True, null=True, max_length=1)
    frozen_b0 = models.FloatField(blank=True, null=True, help_text="If forced through zero, B0 has to be 0")
    frozen_b1 = models.FloatField(blank=True, null=True)
    frozen_b2 = models.FloatField(blank=True, null=True)
    frozen_exp_a = models.FloatField(blank=True, null=True)
    frozen_exp_b = models.FloatField(blank=True, null=True)
    frozen_comment = models.CharField(max_length=255, blank=True, null=True)
    frozen_import = models.CharField(max_length=255, blank=True, null=True)
    deepfr_abs_min_prefix = models.CharField(max_length=5, blank=True, null=True)
    deepfr_abs_min = models.FloatField(blank=True, null=True)
    deepfr_abs_max_prefix = models.CharField(max_length=5, blank=True, null=True)
    deepfr_abs_max = models.FloatField(blank=True, null=True)
    deepfr_eq_type = models.CharField(choices=EQTypeChoices,blank=True, null=True, max_length=1)
    deepfr_b0 = models.FloatField(blank=True, null=True, help_text="If forced through zero, B0 has to be 0")
    deepfr_b1 = models.FloatField(blank=True, null=True)
    deepfr_b2 = models.FloatField(blank=True, null=True)
    deepfr_exp_a = models.FloatField(blank=True, null=True)
    deepfr_exp_b = models.FloatField(blank=True, null=True)
    deepfr_comment = models.CharField(max_length=255, blank=True, null=True)
    deepfr_import = models.CharField(max_length=255, blank=True, null=True)
    ultradeepfr_abs_min_prefix = models.CharField(max_length=5, blank=True, null=True)
    ultradeepfr_abs_min = models.FloatField(blank=True, null=True)
    ultradeepfr_abs_max_prefix = models.CharField(max_length=5, blank=True, null=True)
    ultradeepfr_abs_max = models.FloatField(blank=True, null=True)
    ultradeepfr_eq_type = models.CharField(choices=EQTypeChoices,blank=True, null=True, max_length=1)
    ultradeepfr_b0 = models.FloatField(blank=True, null=True, help_text="If forced through zero, B0 has to be 0")
    ultradeepfr_b1 = models.FloatField(blank=True, null=True)
    ultradeepfr_b2 = models.FloatField(blank=True, null=True)
    ultradeepfr_exp_a = models.FloatField(blank=True, null=True)
    ultradeepfr_exp_b = models.FloatField(blank=True, null=True)
    ultradeepfr_comment = models.CharField(max_length=255, blank=True, null=True)
    ultradeepfr_import = models.CharField(max_length=255, blank=True, null=True)
    stabilizer = models.CharField(max_length=255, blank=True, null=True)
    # samplegroup = models.ForeignKey(StabilitySampleGroup, on_delete=models.CASCADE, blank=True, null=True)
    stab_platform = models.ForeignKey(Platform, on_delete=models.CASCADE, blank=True, null=True)
    stab_analyt_method = models.ForeignKey(AnalytMethod, on_delete=models.CASCADE, blank=True, null=True)
    stab_literature = models.ManyToManyField(Literature)
    stab_comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.analyte_name

    class Meta:
        verbose_name = "Stability"
        verbose_name_plural = "Stabilities"
class Analyte(models.Model):
    aid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    abbr = models.CharField(max_length=255, blank=True, null=True)
    details = models.CharField(max_length=255, blank=True, null=True)
    loinc_num = models.CharField(max_length=50, blank=True, null=True)
    loinc_component = models.CharField(max_length=255, blank=True, null=True)
    loinc_short_name= models.CharField(max_length=255, blank=True, null=True)
    loinc_long_name= models.CharField(max_length=255, blank=True, null=True)
    loinc_class = models.CharField(max_length=255, blank=True, null=True)
    loinc_url = models.URLField(blank=True, null=True)
    unit = models.ManyToManyField(Unit)
    category = models.ManyToManyField(Category)
    tube_not = models.ManyToManyField(SampleType, blank=True, related_name='tube_not_sampletype')
    tube_maybeposs = models.ManyToManyField(SampleType, blank=True, related_name='tube_maybe_sampletype')
    tube_possible = models.ManyToManyField(SampleType, blank=True, related_name='tube_possible_sampletype')
    tube_recomm = models.ManyToManyField(SampleType, blank=True, related_name='tube_recomm_sampletype')
    tube_not_comment = models.CharField(max_length=255, blank=True, null=True)
    tube_maybeposs_comment = models.CharField(max_length=255, blank=True, null=True)
    tube_possible_comment = models.CharField(max_length=255, blank=True, null=True)
    tube_recomm_comment = models.CharField(max_length=255, blank=True, null=True)
    cvi = models.FloatField(blank=True, null=True)
    cvi_comment = models.CharField(max_length=255, blank=True, null=True)
    cvi_literature = models.ManyToManyField(Literature, related_name='cvi_literature')
    bhl_min = models.FloatField(blank=True, null=True)
    bhl_max = models.FloatField(blank=True, null=True)
    bhl_comment = models.CharField(max_length=255, blank=True, null=True)
    bhl_literature = models.ManyToManyField(Literature, related_name='bhl_literature')
    stability = models.ManyToManyField(Stability)
    annotation = models.CharField(max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}, {self.details}"