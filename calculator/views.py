
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    TemplateView,
)
from django.core import validators
from .forms import *
from django.shortcuts import redirect, render
from .models import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm


class ResultsView(DetailView):
    template_name = "calculator/results.html"
    model = Setting
    context_object_name = "setting"

    # extra_context={'subjects': Subject.objects.all()}, {'results': Result.objects.all()}
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subjects = Subject.objects.filter(setting=self.object)
        durations_val = Duration.objects.all().values()
        durations_data = pd.DataFrame(durations_val)

        results_val = Result.objects.all().values()
        results_data = pd.DataFrame(results_val)
        # https://365datascience.com/tutorials/python-tutorials/linear-regression/

        merged_res_dur = pd.merge(
            results_data,
            durations_data,
            left_on="duration_id",
            right_on="id",
            how="inner",
        )
        cols = merged_res_dur["duration_id"].nunique()  # number of timepoints
        rows = merged_res_dur["subject_id"].nunique()  # number of subjects
        # ----------------Numpy-Arrays

        context["results_array"] = np.array(merged_res_dur)
        # print(results_array.size, results_array.shape)
        # mean_panda=merged_res_dur['value'].mean()
        # mean_numpy = np.mean(merged_res_dur, axis=0)
        # # mean_scipy = sp.stats.norm.mean(merged_res_dur, axis=1)
        # print(mean_numpy[1], mean_panda)
        # print(results_array)
        y = merged_res_dur["value"]  # dependent variable
        x1 = merged_res_dur["seconds"]  # independent variable
        # for timepoints in x1:
        #     values = timepoints
        #     print(values)

        # MatPlotLib Scattergramm:
        # plt.scatter(x1, y)
        # plt.xlabel('Seconds', fontsize=20)
        # plt.ylabel('Results', fontsize=20)
        # plt.show()

        x = sm.add_constant(x1)  # add a row of ones as constant
        model = sm.OLS(y, x)
        results = model.fit()  # OLS = Ordinary Least Squares
        statistics_extended = results.summary()

        # Extract parameters from summary
        b0 = results.params[0]  # constant coeffitient / Intercept
        b1 = results.params[1]  # seconds coefficient / Slope
        b0_r = round(b0, 5)
        b1_r = round(b1, 5)
        reg_eq_lin = (
            "y = " + str(b0_r) + " + x1 * " + str(b1_r)
        )  # equation linear regression: y = b0 + x1*b1

        context["slope"] = b1_r
        context["intercept"] = b0_r
        context["f_value"] = (results.fvalue)  # Essentially, it asks, is this a useful variable? Does it help us explain the variability we have in this case?
        context["f_p_value"] = results.f_pvalue
        # context['std_err'] = results.params[0,1]
        context["r_square"] = results.rsquared

        # print(duration_cat2)
        # df["Name"].astype('category')

        # df = pd.DataFrame({"A": list("abca"), "B": list("bccd")}, dtype="category")

        # avg_tot = results_val['value'].mean()
        # avg_tot_duration = results_duration[duration_unit_cat.categories]
        # print(results_duration.to_html)
        # print(results_data['value'].std())
        # print(duration_data.sort_values(by='seconds', ascending=True).to_html)

        context.update(
            {
                "results": Result.objects.all(),
                "durations": Duration.objects.all(),
                "replicates": Replicate.objects.all(),
                "results_df": merged_res_dur.to_html,
            }
        )
        context["subjects"] = subjects
        context["statistics_extended"] = statistics_extended
        context["reg_eq_lin"] = reg_eq_lin
        return context

        # sns.lineplot(
        #     data=merged_res_dur,
        #     x='duration_id',#TODO: pass duration and unit instead of ID
        #     y='value',
        #     hue='subject_id',
        #     # estimator='mean',
        #     # ci=95,
        #
        # )
        # sns.relplot(
        #     data=merged_res_dur,
        #     x='duration_id',  # TODO: pass duration and unit instead of ID
        #     y='value',
        #     # hue='duration_id',
        #     kind='line',
        #     err_style='band',
        # )
        # sns.boxplot(
        #     data=merged_res_dur,
        #     x='duration_id',  # TODO: pass duration and unit instead of ID
        #     y='value',
        #
        #
        # )
        #
        # plt.title("kaka")
        # plt.show()

        # sns.relplot(
        #     data=results_data.sort_values(by=[]),
        #     x='duration_id',
        #     y='value',
        #     kind='line'
        # )
        #
        # plt.show()

        # titanic = sns.load_dataset('titanic')
        #
        # plt.figure(figsize=(8, 5))
        # sns.boxplot(x='class', y='age', data=titanic, palette='rainbow')
        # plt.title("Age by Passenger Class, Titanic")
        #
        # plt.show()


class DashboardView(ListView):
    model = Instrument

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sample = Sample.objects.all()
        context["samples"] = sample
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
        return self.render_to_response({"value_formset": formset})

    def post(self, *args, **kwargs):
        formset = ValueFormset(data=self.request.POST)
        # Check if submitted forms are valid
        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy("add_results"))

        return self.render_to_response({"value_formset": formset})

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
    template_name = "calculator/calculator_form.html"

    ### ContextMixin
    def get_context_data(self, **kwargs):
        """Adds extra content to our template"""
        context = super(MultiInputView, self).get_context_data(**kwargs)

        context["setting_form"] = SettingForm(
            prefix="SettingForm",
            # Multiple 'submit' button paths should be handled in form's .save()/clean()
            data=self.request.POST
            if bool(
                set(
                    [
                        "SettingForm-submit",
                    ]
                ).intersection(self.request.POST)
            )
            else None,
        )

        context["duration_form"] = DurationForm(
            prefix="duration",
            data=self.request.POST if "Duration-submit" in self.request.POST else None,
            files=self.request.FILES
            if "Duration-submit" in self.request.POST
            else None,
        )

        context["value_form"] = ValueForm(
            prefix="value",
            data=self.request.POST if "Value-submit" in self.request.POST else None,
            files=self.request.FILES if "Value-submit" in self.request.POST else None,
        )

        # context['value_form'] = ValueForm()
        return context

    ### NegotiationGroupDetailView
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if context["setting_form"].is_valid():
            instance = context["setting_form"].save()
            # messages.success(request, 'Setting saved.'.format(instance.pk))
        elif context["duration_form"].is_valid():
            instance = context["parameter_form"].save()
            # messages.success(request, 'Duration setting has been saved.'.format(instance.pk))
        elif context["value_form"].is_valid():
            instance = context["value_form"].save()
            # messages.success(request, 'Value has been saved.'.format(instance.pk))
            # advise of any errors

        else:
            # messages.error('Error(s) encountered during form processing, please review below and re-submit')
            pass
        return self.render_to_response(context)
