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





class ValueInline(admin.StackedInline):
    model = Value
    extra = 1

class DurationAdmin(admin.ModelAdmin):
    model = Duration
    exclude = ('value',)
    inlines = [ValueInline]

class DurationInline(admin.TabularInline):
    model = Duration
    exclude = ('value',)
    extra = 1

class SubjectAdmin(admin.ModelAdmin):
    model = Subject
    inlines = [DurationInline]
    fields = None


class SubjectInline(admin.TabularInline):
    model = Subject
    exclude = ('value',)
    extra = 1

class SettingAdmin(admin.ModelAdmin):
    model = Setting
    exclude = ('subject',)
    inlines = [SubjectInline]




class FooAdmin(admin.ModelAdmin):
    form = InstrumentForm
    add_form_template = "calculator/instrument_form.html"
    change_form_template = "calculator/instrument_update.html"







class UserAdminArea(admin.AdminSite):
    site_header = 'User Dashboard'
    site_title = 'EFLM Stability Calculator Dashboard'


user_dashboard = UserAdminArea(name='UserAdmin')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Parameter)
admin.site.register(Instrument, FooAdmin)
admin.site.register(Condition, ConditionAdmin)
admin.site.register(Sample)
admin.site.register(Duration, DurationAdmin)
# admin.site.register(Population)
admin.site.register(Setting, SettingAdmin)
admin.site.register(Subject, SubjectAdmin)


user_dashboard.register(Parameter)
user_dashboard.register(Instrument, InstrumentAdmin)
user_dashboard.register(Condition, ConditionAdmin)
user_dashboard.register(Sample)
user_dashboard.register(Duration, DurationAdmin)
# user_dashboard.register(Population)
user_dashboard.register(Setting, SettingAdmin)
user_dashboard.register(Subject, SubjectAdmin)