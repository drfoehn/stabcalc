from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.core import validators
from .forms import *
from django.shortcuts import redirect, render
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

class SettingAddView(CreateView):
    template_name = "calculator/result_form.html"
    model = Setting
    form_class = SettingForm
    # success_url = "/dashboard"

class ValuesAddView(TemplateView):
    template_name = "calculator/result_form.html"
    # model = Result
    # form_class = ResultForm
    # success_url = "/dashboard"

    # Define method to handle GET request
    def get(self, *args, **kwargs):
        # Create an instance of the formset
        formset = ValueFormset(queryset=Result.objects.none())
        return self.render_to_response({'value_formset': formset})

    def post(self, *args, **kwargs):
        formset = ValueFormset(data=self.request.POST)
        # Check if submitted forms are valid
        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy("add_results"))

        return self.render_to_response({'value_formset': formset})


    # def post(self, request, *args, **kwargs):
    #     return super().post(request, *args, **kwargs)

# def result_view(request):
#     if request.method == 'POST':
#         Order=formset_factory(ResultForm,extra=4)
#         formset=Order(request.POST)
#         if formset.is_valid():
#             for form in formset:
#                 value=form.cleaned_data.get('value')
#                 if value:
#                     Result(value=value).save()
#             return redirect(result_view)
#     else:
#         Order=formset_factory(ResultForm,extra=4)
#         formset=Order()
#         return render(request,'calculator/result_form.html',{'formset':formset})


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

class MultiInputView(TemplateView):
    ### TemplateResponseMixin
    template_name = 'calculator/calculator_form.html'

    ### ContextMixin
    def get_context_data(self, **kwargs):
        """ Adds extra content to our template """
        context = super(MultiInputView, self).get_context_data(**kwargs)

        context['setting_form'] = SettingForm(
            prefix='SettingForm',
        # Multiple 'submit' button paths should be handled in form's .save()/clean()
        data = self.request.POST if bool(set(['SettingForm-submit',]).intersection(
            self.request.POST)) else None,
        )

        context['duration_form'] = DurationForm(
            prefix='duration',
        data = self.request.POST if 'Duration-submit' in self.request.POST else None,
               files = self.request.FILES if 'Duration-submit' in self.request.POST else None

        )

        context['value_form'] =ValueForm(
            prefix='value',
            data=self.request.POST if 'Value-submit' in self.request.POST else None,
            files=self.request.FILES if 'Value-submit' in self.request.POST else None

        )

        # context['value_form'] = ValueForm()
        return context

    ### NegotiationGroupDetailView
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if context['setting_form'].is_valid():
            instance = context['setting_form'].save()
            # messages.success(request, 'Setting saved.'.format(instance.pk))
        elif context['duration_form'].is_valid():
            instance = context['parameter_form'].save()
            # messages.success(request, 'Duration setting has been saved.'.format(instance.pk))
        elif context['value_form'].is_valid():
            instance = context['value_form'].save()
            # messages.success(request, 'Value has been saved.'.format(instance.pk))
            # advise of any errors

        else:
            # messages.error('Error(s) encountered during form processing, please review below and re-submit')
            pass
        return self.render_to_response(context)