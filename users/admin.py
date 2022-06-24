from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import LabUser


class UserAdminConfig(UserAdmin):
    model =LabUser
    search_fields = ['laboratory_name', 'country', 'city', 'user_name', 'email']
    list_filter = ['laboratory_name', 'country', 'is_active', 'is_staff']
    ordering = ['date_joined']
    list_display = ['laboratory_name', 'country', 'user_name', 'is_active', 'is_staff']

    fieldsets = (

        ('User-Detail', {'fields': ('user_name', 'email', 'password')}),
        ('Laboratory', {'fields': ('laboratory_name', 'clinics', 'country', 'city')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),

    )

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('laboratory_name', 'clinics', 'country', 'city', 'user_name', 'password', 'is_active', 'is_staff')
        }),

    )


admin.site.register(LabUser, UserAdminConfig)