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


class UserAdminArea(admin.AdminSite):
    site_header = 'User Dashboard'
    site_title = 'EFLM Stability Calculator Dashboard'

user_dashboard = UserAdminArea(name='UserAdmin')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Parameter)
admin.site.register(Instrument)
admin.site.register(Condition)
admin.site.register(Sample)
admin.site.register(Duration)
admin.site.register(Population)
admin.site.register(Result)

user_dashboard.register(Parameter)
user_dashboard.register(Instrument)
user_dashboard.register(Condition)
user_dashboard.register(Sample)
user_dashboard.register(Duration)
user_dashboard.register(Population)
# user_dashboard.register(Result)