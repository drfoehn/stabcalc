from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import *

# Register your models here.

class LabUserInline(admin.StackedInline):
    model = LabUser
    can_delete = False

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (LabUserInline,)

class ConditionAdmin(admin.ModelAdmin):
    model = Condition
    list_display = ['temperature', 'light', 'air', 'agitation']

class InstrumentAdmin(admin.ModelAdmin):
    model = Instrument
    list_display = ['name', 'manufacturer']

class ParameterAdmin(admin.ModelAdmin):
    model = Parameter


class ResultAdmin(admin.ModelAdmin):
    model = Result
    extra = 1

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


class UserAdminArea(admin.AdminSite):
    site_header = 'User Dashboard'
    site_title = 'EFLM Stability Calculator Dashboard'

user_dashboard = UserAdminArea(name='UserAdmin')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Parameter)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(Condition, ConditionAdmin)
admin.site.register(Sample)
admin.site.register(Duration)
admin.site.register(Population)
admin.site.register(Result, ResultAdmin)
admin.site.register(Subject)

user_dashboard.register(Parameter)
user_dashboard.register(Instrument, InstrumentAdmin)
user_dashboard.register(Condition, ConditionAdmin)
user_dashboard.register(Sample)
user_dashboard.register(Duration)
user_dashboard.register(Population)
user_dashboard.register(Result, ResultAdmin)
user_dashboard.register(Subject)