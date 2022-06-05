from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import *

# Register your models here.
# class ParameterAdmin(admin.ModelAdmin):
#     model = ParameterModel



# class ResultInline(admin.StackedInline):
#     model = Result
#     extra = 1
#
#
#
# class ParameterAdmin(admin.ModelAdmin):
#     # list_display = ("parameter", "created", "updated", "is_published")
#     inlines = [ResultInline]
#     fields = ("name", "unit")




admin.site.register(Parameter)
admin.site.register(Instrument)
admin.site.register(Condition)
admin.site.register(Sample)
admin.site.register(Duration)
admin.site.register(Result)
