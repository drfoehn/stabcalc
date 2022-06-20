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
from sklearn.preprocessing import PolynomialFeatures
import math
from patsy.highlevel import dmatrices


class ResultsView(DetailView):
    template_name = "calculator/results.html"
    model = Setting
    context_object_name = "setting"

    # extra_context={'subjects': Subject.objects.all()}, {'results': Result.objects.all()}
    def get_context_data(self, **kwargs):
        global single_results_value, single_results_duration
        context = super().get_context_data(**kwargs)
        subjects = Subject.objects.filter(setting=self.object)
        durations_val = Duration.objects.all().values()
        durations_data = pd.DataFrame(durations_val)
        results = Result.objects.filter(setting=self.object)
        results_val = results.values()
        results_data = pd.DataFrame(results_val)
        parameter = Parameter.objects.filter(setting=self.object).values('name', 'unit')


        # ---------------------------Get deviation data for each subject setting and time individually
        deviation_dict: dict[int, dict[int, int]] = {}
        for subject in subjects:
            if not subject.id in deviation_dict:
                deviation_dict[subject.id] = {}
            for duration in self.object.duration_set.all():
                deviation_dict[subject.id][duration.seconds] = subject.deviation(duration)

        deviation_array = pd.DataFrame(deviation_dict)
        deviation_array.index.name = "duration"

        # https://www.delftstack.com/howto/python-pandas/how-to-iterate-through-rows-of-a-dataframe-in-pandas/

        #################################### VARIABLES ######################################

        # ---------------------------Relative Deviation from Baseline
        y_rel = []
        x1_rel = []
        for (duration, results) in deviation_array.iterrows():
            for result in results:
                if not math.isnan(result):  # pandas converts None-values to "nan" - this function excludes those values
                    y_rel.append(result)
                    x1_rel.append(duration)

        # ----------------------Absolute values
        # ----------------------Merge data absolute results + duration
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

        # -------------------Variable absolute results
        y_abs = merged_res_dur["value"]  # dependent variable
        x1_abs = merged_res_dur["seconds"]  # independent variable

        # --------------------------Log transformation
        x1_rel_log = []
        for xr in x1_rel:
            if xr:
                xr = math.log(xr)
            x1_rel_log.append(xr)

        # print(x1_rel_log)

        x1_abs_log = []
        for xa in x1_abs:
            if xa:
                xa = math.log(xa)
            x1_abs_log.append(xa)

        # print(x1_abs_log)
        # print(x1_abs)
        # print(y_abs)

        ################################# REGRESSION ANALYSIS ######################################

        # https://365datascience.com/tutorials/python-tutorials/linear-regression/

        ## --------------------Explanation of statistics summary:
        # https://medium.com/swlh/interpreting-linear-regression-through-statsmodels-summary-4796d359035a
        # TODO: But why are there four different versions of Region when we only input one? Simply put, the formula expects continuous values in the form of numbers. By inputting region with data points as strings, the formula separates each string into categories and analyzes the category separately. Formatting your data ahead of time can help you organize and analyze this properly.

        # -----------------------LINEAR----------------------------------------

        vars = ['value', 'seconds']
        merged_res_dur = merged_res_dur[vars]
        merged_res_dur = merged_res_dur.dropna()
        y, X = dmatrices('value~seconds', data=merged_res_dur, return_type='dataframe')
        mod = sm.OLS(y, X)  # Describe model
        res = mod.fit()  # Fit model
        # print(res.summary())  # Summarize model

        # print(res.params)
        r_squared_lin = res.rsquared
        context["r_squared_lin"] = r_squared_lin
        r_squared_lin_adj = res.rsquared_adj
        context["r_squared_lin_adj"] = r_squared_lin_adj
        X = merged_res_dur.iloc[:, 1]  # seconds
        y = merged_res_dur.iloc[:, 0]  # value

        # # Calculate Regression equation - polynomial 2rd degree
        # eq_model_lin = np.poly1d(np.polyfit(X, y, 1))
        # a = eq_model_lin

        # Calculate Regression equation - polynomial 2rd degree - https://www.statology.org/polynomial-regression-python/

        eq2 = np.poly1d(np.polyfit(X, y, 2))
        context["eq_model_poly2"] = str("y = " + str(round(eq2[3], 5)) + " * x^3 + " + str(round(eq2[2], 5))
                                        + " * x^2 + " + str(round(eq2[1], 5)) + " * x + " + str(round(eq2[0], 5)))
        # FIXME: Only the last two numbers get rounded on 5 digits ?!?!?

        # Calculate r_squared
        results = {}
        coeffs = np.polyfit(X, y, 2)
        p = np.poly1d(coeffs)
        # calculate r-squared
        yhat = p(X)
        ybar = np.sum(y) / len(y)
        ssreg = np.sum((yhat - ybar) ** 2)
        sstot = np.sum((y - ybar) ** 2)
        r_squared_poly2 = ssreg / sstot

        context["r_squared_poly2"] = r_squared_poly2

        # Calculate Regression equation - polynomial 3rd degree

        eq3 = np.poly1d(np.polyfit(X, y, 3))
        context["eq_model_poly3"] = str("y = " + str(round(eq3[3], 5)) + " * x^3 + " + str(round(eq3[2], 5))
                                        + " * x^2 + " + str(round(eq3[1], 5)) + " * x + " + str(round(eq3[0], 5)))
        #FIXME: Only the last two numbers get rounded on 5 digits ?!?!?

        # Calculate r_squared
        results = {}
        coeffs = np.polyfit(X, y, 3)
        p = np.poly1d(coeffs)
        # calculate r-squared
        yhat = p(X)
        ybar = np.sum(y) / len(y)
        ssreg = np.sum((yhat - ybar) ** 2)
        sstot = np.sum((y - ybar) ** 2)
        r_squared_poly3 = ssreg / sstot

        context["r_squared_poly3"] = r_squared_poly3

        # Rainbow test for linearity (the null hypothesis is that the relationship is properly modelled as linear);
        # first number is an F-statistic and that the second is the p-value.

        rainbow_test = sm.stats.linear_rainbow(res)

        # print(rainbow_test)

        # Test assumed normal or exponential distribution using Lilliefors’ test.        #
        # Lilliefors’ test is a Kolmogorov - Smirnov test with estimated parameters.
        # first number: ksstatfloat Kolmogorov - Smirnov test  statistic with estimated mean and variance.
        # second number: pvaluefloat   If  the pvalue is lower  than some threshold, e.g. 0.05, then  we can  reject the   Null hypothesis  that  the  sample comes from a normal distribution.

        ks = sm.stats.diagnostic.kstest_normal(y, dist='norm', pvalmethod='table')

        # print(ks)

        # TODO: Predicting values from regression: https://towardsdatascience.com/linear-regression-with-python-and-numpy-25d0e1dd220d
        # TODO:  ANOVA: https://www.statsmodels.org/dev/examples/notebooks/generated/interactions_anova.html

        # ------------------------Absolute

        x1_abs = sm.add_constant(
            x1_abs)  # add a row of ones as constant #TODO: Is this line necessary ? - https://365datascience.com/tutorials/python-tutorials/linear-regression/
        model = sm.OLS(y_abs, x1_abs)
        results_abs = model.fit()  # OLS = Ordinary Least Squares
        context["statistics_extended_abs_lin"] = results_abs.summary()

        # -------------------------Extract single parameters from summary - linear regression
        b0_abs_lin = results_abs.params[0]  # constant coefficient / Intercept
        b1_abs_lin = results_abs.params[1]  # seconds coefficient / Slope
        b0_r_abs_lin = round(b0_abs_lin, 5)
        context["intercept_abs_lin"] = b0_r_abs_lin
        b1_r_abs_lin = round(b1_abs_lin, 5)
        context["slope_abs_lin"] = b1_r_abs_lin
        context["reg_eq_abs_lin"] = (
                "y = " + str(b0_r_abs_lin) + " + x1 * " + str(b1_r_abs_lin)
        )  # equation linear regression: y = b0 + x1*b1

        # --------------------------relative

        x_rel = sm.add_constant(x1_rel)  # add a row of ones as constant
        model = sm.OLS(y_rel, x_rel)
        results_rel = model.fit()  # OLS = Ordinary Least Squares
        context["statistics_extended_rel_lin"] = results_rel.summary()

        # -------------------------Extract single parameters from summary - linear regression
        b0_rel_lin = results_rel.params[0]  # constant coefficient / Intercept
        b1_rel_lin = results_rel.params[1]  # seconds coefficient / Slope
        b0_r_rel_lin = round(b0_rel_lin, 5)
        context["intercept_rel_lin"] = b0_r_rel_lin
        b1_r_rel_lin = round(b1_rel_lin, 5)
        context["slope_rel_lin"] = b1_r_rel_lin
        context["reg_eq_rel_lin"] = (
                "y = " + str(b0_r_rel_lin) + " + x1 * " + str(b1_r_rel_lin)
        )  # equation linear regression: y = b0 + x1*b1

        # ------------------------Absolute log

        x1_abs_log = sm.add_constant(
            x1_abs_log)  # add a row of ones as constant #TODO: Is this line necessary ? - https://365datascience.com/tutorials/python-tutorials/linear-regression/
        model = sm.OLS(y_abs, x1_abs_log)
        results_abs_log = model.fit()  # OLS = Ordinary Least Squares
        context["statistics_extended_abs_lin_log"] = results_abs_log.summary()

        # -------------------------Extract single parameters from summary - linear regression
        b0_abs_lin_log = results_abs_log.params[0]  # constant coefficient / Intercept
        b1_abs_lin_log = results_abs_log.params[1]  # seconds coefficient / Slope
        b0_r_abs_lin_log = round(b0_abs_lin_log, 5)
        context["intercept_abs_lin_log"] = b0_r_abs_lin_log
        b1_r_abs_lin_log = round(b1_abs_lin_log, 5)
        context["slope_abs_lin_log"] = b1_r_abs_lin_log
        context["reg_eq_abs_lin"] = (
                "y = " + str(b0_r_abs_lin_log) + " + x1 * " + str(b1_r_abs_lin_log)
        )  # equation linear regression: y = b0 + x1*b1

        # --------------------------relative log

        x_rel_log = sm.add_constant(x1_rel_log)  # add a row of ones as constant
        model = sm.OLS(y_rel, x_rel_log)
        results_rel_log = model.fit()  # OLS = Ordinary Least Squares
        context["statistics_extended_rel_lin_log"] = results_rel_log.summary()

        # -------------------------Extract single parameters from summary - linear regression
        b0_rel_lin_log = results_rel_log.params[0]  # constant coefficient / Intercept
        b1_rel_lin_log = results_rel_log.params[1]  # seconds coefficient / Slope
        b0_r_rel_lin_log = round(b0_rel_lin_log, 5)
        context["intercept_rel_lin_log"] = b0_r_rel_lin_log
        b1_r_rel_lin_log = round(b1_rel_lin_log, 5)
        context["slope_rel_lin_log"] = b1_r_rel_lin_log
        context["reg_eq_lin_log"] = (
                "y = " + str(b0_r_rel_lin_log) + " + x1 * " + str(b1_r_rel_lin_log)
        )  # equation linear regression: y = b0 + x1*b1

        #

        # --------------------------Calculate best fitting model

        r_sq_list =[r_squared_lin, r_squared_poly2, r_squared_poly3]
        best_fit= max(r_sq_list)
        context["best_fit"] = str(str(round(best_fit*100, 2)) + " %")

        def best_fit_model() -> str:
            if r_squared_lin == best_fit:
                return 'Linear Regression Model'
            elif r_squared_poly2 == best_fit:
                return 'Polynomial Regression Model 2° degree'
            else:
                return 'Polynomial Regression Model 3° degree'

        context["best_fit_model"] = best_fit_model()

        context["interpretation_1"] = '1 hour of sample storage under the tested conditions causes the the ' + str(parameter.values('name')[0]['name']) +  ' level to change by ' + str(round(res.params[1]*3600, 3)) + ' ' +str(parameter.values('unit')[0]['unit'])



        # --------------------MatPlotLib Scattergramm:
        # plt.scatter(x1_rel, y_rel)
        # plt.xlabel('Seconds', fontsize=20)
        # plt.ylabel('Results', fontsize=20)
        # plt.show()

        # ------------------------Return context

        context["f_value"] = (
            results_abs.fvalue)  # Essentially, it asks, is this a useful variable? Does it help us explain the variability we have in this case?
        context["f_p_value"] = results_abs.f_pvalue
        # context['std_err'] = results.params[0,1]
        context["r_square"] = results_abs.rsquared
        context.update(
            {
                "results": results,
                "durations": Duration.objects.all(),
                "replicates": Replicate.objects.all(),

            }
        )
        context["subjects"] = subjects

        return context


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
