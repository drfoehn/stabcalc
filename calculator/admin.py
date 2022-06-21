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

class InstrumentAdmin(admin.ModelAdmin):
    model = Instrument
    exclude = ('author',)
    list_display = ['name', 'manufacturer']

class ConditionAdmin(admin.ModelAdmin):
    model = Condition
    list_display = ['temperature', 'light', 'air', 'agitation', 'other_Condition']

class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 1

# TODO: Prepopulate Duration filed with all durautions from the setting (Custom validation? Override initial?)


class DurationInline(admin.TabularInline):
    model = Duration
    extra = 1

class ResultInline(admin.StackedInline):
    model = Result
    extra = 1

class ReplicateInline(admin.TabularInline):
    model = Replicate
    extra = 1

class SettingAdmin(admin.ModelAdmin):
    model = Setting
    exclude = ('subject',)
    inlines = [SubjectInline]

class SubjectAdmin(admin.ModelAdmin):
    model = Subject
    # inlines = [ResultInline]
    # inlines = [DurationInline]
    exclude = ('duration',)

class DurationAdmin(admin.ModelAdmin):
    model = Duration
    exclude = ('value', 'subject')
    # ordering = ["seconds"]
    # inlines = [ResultInline]

class ResultAdmin(admin.ModelAdmin):
    model = Result


class ReplicateAdmin(admin.ModelAdmin):
    inlines = [ResultInline]

# class InstrumentAdmin(admin.ModelAdmin):
#     form = InstrumentForm
#     add_form_template = "calculator/instrument_form.html"
#     change_form_template = "calculator/instrument_update.html"


class UserAdminArea(admin.AdminSite):
    site_header = 'User Dashboard'
    site_title = 'EFLM Stability Calculator Dashboard'


user_dashboard = UserAdminArea(name='UserAdmin')


# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
admin.site.register(Parameter)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(Condition, ConditionAdmin)
admin.site.register(Sample)
admin.site.register(Duration, DurationAdmin)
# admin.site.register(Population)
admin.site.register(Setting, SettingAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Replicate,ReplicateAdmin)


user_dashboard.register(Parameter)
user_dashboard.register(Instrument, InstrumentAdmin)
user_dashboard.register(Condition, ConditionAdmin)
user_dashboard.register(Sample)
user_dashboard.register(Duration, DurationAdmin)
# user_dashboard.register(Population)
user_dashboard.register(Setting, SettingAdmin)
user_dashboard.register(Subject, SubjectAdmin)
user_dashboard.register(Result, ResultAdmin)