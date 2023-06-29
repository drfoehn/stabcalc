from django.contrib import admin

from django.contrib import admin
from database.models import *

class AnalyteAdmin(admin.ModelAdmin):
    model = Analyte

class LiteratureAdmin(admin.ModelAdmin):
    model = Literature
    list_display = ['authors', 'title']

class PlatformAdmin(admin.ModelAdmin):
    model = Platform

class SampleGroupAdmin(admin.ModelAdmin):
    model = SampleGroup

class SampleTypeAdmin(admin.ModelAdmin):
    model = SampleType
    list_display = ['name',
                    'group']

class UnitAdmin(admin.ModelAdmin):
    model = Unit

class AnalytMethodAdmin(admin.ModelAdmin):
    model=AnalytMethod

class StabilityAdmin(admin.ModelAdmin):
    model = Stability


admin.site.register(Analyte, AnalyteAdmin)
admin.site.register(Literature, LiteratureAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(SampleType, SampleTypeAdmin)
admin.site.register(SampleGroup, SampleGroupAdmin)
admin.site.register(AnalytMethod, AnalytMethodAdmin)
admin.site.register(Stability, StabilityAdmin)