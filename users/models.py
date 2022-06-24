from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, user_name, email, password, city, country, laboratory_name, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(user_name, email, password, city, country, laboratory_name, **other_fields)

    def create_user(self, user_name, email, password, city, country, laboratory_name, **other_fields):

        if not email:
            raise ValueError(_('Please provide an e-mail address'))

        email = self.normalize_email(email)
        city = city
        country = country
        laboratory_name = laboratory_name

        user = self.model(email=email, user_name=user_name, country=country, city=city, laboratory_name=laboratory_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

class LabUser(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(verbose_name='E-Mail', unique=True)
    laboratory_name = models.CharField(_('Name of Laboratory'), max_length=255)
    clinics = models.CharField(max_length=255, verbose_name=_('Name of the Clinic'), blank=True)
    country = CountryField(verbose_name=_('Country'))
    city = models.CharField(max_length=255, verbose_name=_('City'))
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email', 'laboratory_name', 'country', 'city']

    def __str__(self):
        return f'{self.laboratory_name}, {self.user_name}'

