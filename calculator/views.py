from bokeh.models import Range1d
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.core import validators
from .forms import *
from django.shortcuts import redirect, render
from .models import *
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components

class ResultsView(DetailView):
    template_name = 'calculator/results.html'
    model = Setting
    context_object_name = "setting"

    # extra_context={'subjects': Subject.objects.all()}, {'results': Result.objects.all()}
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subjects = Subject.objects.filter(setting=self.object)


        # average = Subject.average(subjects, Duration)

        # create some data
        x1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        y1 = [0, 8, 2, 4, 6, 9, 5, 6, 25, 28, 4, 7]
        x2 = [2, 5, 7, 15, 18, 19, 25, 28, 9, 10, 4]
        y2 = [2, 4, 6, 9, 15, 18, 0, 8, 2, 25, 28]
        x3 = [0, 1, 0, 8, 2, 4, 6, 9, 7, 8, 9]
        y3 = [0, 8, 4, 6, 9, 15, 18, 19, 19, 25, 28]

        # select the tools you want
        TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

        # the red and blue graphs share this data range
        xr1 = Range1d(start=0, end=30)
        yr1 = Range1d(start=0, end=30)

        # only the green graph uses this data range
        xr2 = Range1d(start=0, end=30)
        yr2 = Range1d(start=0, end=30)

        # build the figures
        p1 = figure(x_range=xr1, y_range=yr1, tools=TOOLS, width=300, height=300)
        p1.scatter(x1, y1, size=12, color="red", alpha=0.5)

        p2 = figure(x_range=xr1, y_range=yr1, tools=TOOLS, width=300, height=300)
        p2.scatter(x2, y2, size=12, color="blue", alpha=0.5)

        p3 = figure(x_range=xr2, y_range=yr2, tools=TOOLS, width=300, height=300)
        p3.scatter(x3, y3, size=12, color="green", alpha=0.5)

        # plots can be a single Bokeh model, a list/tuple, or even a dictionary
        plots = {'Red': p1, 'Blue': p2, 'Green': p3}

        script, div = components(plots)



        context["results"] = Result.objects.all()
        context["durations"] = Duration.objects.all()
        context["replicates"] = Replicate.objects.all()
        context["subjects"] = subjects
        context["div"] = div
        context["script"] = script






        return context

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