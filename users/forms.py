from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from django_countries.widgets import CountrySelectWidget

from.models import LabUser
from django import forms

class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField()
    laboratory_name = forms.CharField(max_length=255)
    clinics = forms.CharField(max_length=255)
    country = CountryField()
    city = forms.CharField(max_length=255)
    class Meta:
        # model = get_user_model()
        model = LabUser
        fields = (
            'email',
            'laboratory_name',
            'clinics',
            'city',
            'country'
        )

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    laboratory_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    clinics = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = CountryField(blank_label='(Select country)').formfield()
    city = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        # model = get_user_model()
        model = LabUser
        fields = (
            'user_name',
            'password1',
            'password2',
            'email',
            'laboratory_name',
            'clinics',
            'city',
            'country'
        )
        widgets = {'country': CountrySelectWidget()}

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['country'].widget.attrs['class'] = 'form-select'