from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import *
from .forms import *

# Register your models here.
# class SubjectAdmin(admin.ModelAdmin):
#     form = SubjectFormset
    # add_form_template = "photo/admin/my_add_form.html"
    # change_form_template = "photo/admin/my_change_form.html"


# class LabUserInline(admin.StackedInline):
#     model = LabUser
#     can_delete = False

# # Define a new User admin
# class UserAdmin(BaseUserAdmin):
#     inlines = (LabUserInline,)





class ParameterAdmin(admin.ModelAdmin):
    model = Parameter
    list_display = ['name', 'unit']

class InstrumentAdmin(admin.ModelAdmin):
    model = Instrument
    list_display = ['name', 'manufacturer']

class ConditionAdmin(admin.ModelAdmin):
    model = Condition
    list_display = ['temperature', 'light', 'air', 'agitation', 'other_condition']



# TODO: Prepopulate Duration filed with all durautions from the setting (Custom validation? Override initial?)


class SettingAdmin(admin.ModelAdmin):
    model = Setting
    list_display = ['name', 'parameter', 'condition', 'rerun']

class SubjectAdmin(admin.ModelAdmin):
    model = Subject

class SampleAdmin(admin.ModelAdmin):
    model = Sample
    list_display = ['sample_type', 'container_additive','container_material', 'container_dimension', 'container_fillingvolume']

class DurationAdmin(admin.ModelAdmin):
    model = Duration


class ResultAdmin(admin.ModelAdmin):
    model = Result
    list_display = ['value', 'setting', 'duration']


class ResultInline(admin.StackedInline):
    model = Result
    extra = 1


class ReplicateAdmin(admin.ModelAdmin):
    inlines = [ResultInline]


class UserAdminArea(admin.AdminSite):
    site_header = 'User Dashboard'
    site_title = 'EFLM Stability Calculator Dashboard'


# user_dashboard = UserAdminArea(name='UserAdmin')


# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
admin.site.register(Parameter)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(Condition, ConditionAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Duration, DurationAdmin)
# admin.site.register(Population)
admin.site.register(Setting, SettingAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Replicate,ReplicateAdmin)


# user_dashboard.register(Parameter)
# user_dashboard.register(Instrument, InstrumentAdmin)
# user_dashboard.register(Condition, ConditionAdmin)
# user_dashboard.register(Sample)
# user_dashboard.register(Duration, DurationAdmin)
# # user_dashboard.register(Population)
# user_dashboard.register(Setting, SettingAdmin)
# user_dashboard.register(Subject, SubjectAdmin)
# user_dashboard.register(Result, ResultAdmin)