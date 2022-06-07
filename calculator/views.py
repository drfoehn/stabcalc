from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.core import validators
from .forms import *
from django.shortcuts import redirect
from .models import *


class DashboardView(ListView):
    model = Instrument

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            sample = Sample.objects.all()
            context['samples'] = sample
            # Add any other variables to the context here
            ...
            return context

class InstrumentIndex(ListView):
    model = Instrument


class InstrumentAddView(CreateView, SuccessMessageMixin):
    # template_name = "xxx.html"
    model = Instrument
    form_class = InstrumentForm
    success_message = "Instrument saved"

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    # def get_success_url(self):
    #     return HttpResponseRedirect('/')


class InstrumentUpdateView(UpdateView):
    model = Instrument
    form_class = InstrumentForm
    # template_name = 'instrument_update.html'  # templete for updating
    success_url = "/dashboard"


class SampleAddView(CreateView):
    # template_name = "xxx.html"
    model = Sample
    form_class = SampleForm
    success_url = "/dashboard"

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ResultsAddView(CreateView):
    # template_name = "xxx.html"
    model = Result
    form_class = ResultForm
    # success_url = "/dashboard"

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ParameterIndex(ListView):
    model = Parameter


class ParameterDetail(DetailView):
    model = Parameter


class ParameterAddView(CreateView):
    # template_name = "xxx.html"
    model = Parameter
    form_class = ParameterForm

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
