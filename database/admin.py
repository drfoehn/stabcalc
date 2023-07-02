from django.contrib import admin

from django.contrib import admin
from database.models import *

class AnalyteAdmin(admin.ModelAdmin):
    model = Analyte
    ordering = ['name']
    search_fields = ['name']

class LiteratureAdmin(admin.ModelAdmin):
    model = Literature
    list_display = ['authors', 'title']

class PlatformAdmin(admin.ModelAdmin):
    model = Platform

class SpecimenAdmin(admin.ModelAdmin):
    model = Specimen

class SampleTypeAdmin(admin.ModelAdmin):
    model = SampleType
    list_display = ['name']

class UnitAdmin(admin.ModelAdmin):
    model = Unit

class AnalytMethodAdmin(admin.ModelAdmin):
    model=AnalytMethod

class StabilityAdmin(admin.ModelAdmin):
    model = Stability

class CategoryAdmin(admin.ModelAdmin):
    model = Category

class AnalyteSpecimenAdmin(admin.ModelAdmin):
    model = AnalyteSpecimen

admin.site.register(Analyte, AnalyteAdmin)
admin.site.register(Literature, LiteratureAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(SampleType, SampleTypeAdmin)
admin.site.register(Specimen, SpecimenAdmin)
admin.site.register(AnalytMethod, AnalytMethodAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Stability, StabilityAdmin)
admin.site.register(AnalyteSpecimen, AnalyteSpecimenAdmin)