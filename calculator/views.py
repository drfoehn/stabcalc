from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.forms import modelformset_factory  # is grey but still needed for the result_add_view
from datetime import datetime
from wsgiref.util import FileWrapper
import json
from django.utils import timezone
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from statsmodels.stats.power import TTestIndPower
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    TemplateView,
)

from .forms import *
from django.shortcuts import redirect, render, get_object_or_404
from .models import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import math
from patsy.highlevel import dmatrices
from django.http import HttpResponse, HttpResponseForbidden


class ResultsView(DetailView):
    template_name = "calculator/results.html"
    model = Setting
    context_object_name = "setting"

    def get_context_data(self, **kwargs):
        global single_results_value, single_results_duration
        context = super().get_context_data(**kwargs)
        subjects = Subject.objects.filter(settings__in=[self.object])
        durations = Duration.objects.filter(settings__in=[self.object])
        durations_val = durations.values()
        durations_data = pd.DataFrame(durations_val)
        results = Result.objects.filter(setting=self.object)
        results_val = results.values()
        results_data = pd.DataFrame(results_val)
        parameter = ParameterUser.objects.filter(setting=self.object).values('parameter__name', 'parameter__unit')
        setting = self.object
        context['subjects_n'] = Subject.objects.filter(settings__in=[self.object]).count()
        context['durations_n'] = Duration.objects.filter(settings__in=[self.object]).count()
        context['results_n'] = Result.objects.filter(setting=self.object).count()

        # ---------------------------Get deviation data for each subject setting and time individually in a dict
        deviation_dict: dict[int, dict[int, int]] = {}
        for subject in subjects:
            if not subject.id in deviation_dict:
                deviation_dict[subject.id] = {}
                for duration in self.object.durations.all():
                    if setting == self.object:
                        deviation_dict[subject.id][duration.seconds] = subject.deviation(duration, setting)

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

        # print(y_rel)
        # print(x1_rel)
        # ----------------------Absolute values
        # ----------------------Merge data absolute results + duration
        merged_res_dur = pd.merge(
            results_data,
            durations_data,
            left_on="duration_id",
            right_on="id",
            how="inner",
        )

        merged_res_dur['hours'] = (merged_res_dur['seconds'] / 3600)
        context["results_data222"] = merged_res_dur.to_html

        # ----------------Numpy-Arrays
        context["results_array"] = np.array(merged_res_dur)

        # -------------------Variable absolute results
        y_abs = merged_res_dur["value"]  # dependent variable
        x1_abs = merged_res_dur["seconds"]  # independent variable

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
        context["statistics_extended_abs_lin"] = res.summary()

        r_squared_lin = res.rsquared
        context["r_squared_lin"] = r_squared_lin
        r_squared_lin_adj = res.rsquared_adj
        context["r_squared_lin_adj"] = r_squared_lin_adj
        X = merged_res_dur.iloc[:, 1]  # seconds
        y = merged_res_dur.iloc[:, 0]  # value

        # Calculate Regression equation - linear
        eq1 = np.poly1d(np.polyfit(X, y, 1))
        context["eq_model_lin"] = str("y = " + str(round(eq1[1], 5)) + " * x + " + str(round(eq1[0], 5)))

        # predition_lin= sm.ols("y ~ x", data=merged_res_dur).fit()
        # predition_lin.predict(exog=new_values_dict)

        # --------------------------Calculate Regression equation - polynomial 2rd degree - https://www.statology.org/polynomial-regression-python/

        eq2 = np.poly1d(np.polyfit(X, y, 2))
        context["eq_model_poly2"] = str("y = " + str(round(eq2[2], 5))
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

        # ---------------------------------Calculate Regression equation - polynomial 3rd degree

        eq3 = np.poly1d(np.polyfit(X, y, 3))
        context["eq_model_poly3"] = str("y = " + str(round(eq3[3], 5)) + " * x^3 + " + str(round(eq3[2], 5))
                                        + " * x^2 + " + str(round(eq3[1], 5)) + " * x + " + str(round(eq3[0], 5)))

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

        # TODO: Predicting values from regression: https://towardsdatascience.com/linear-regression-with-python-and-numpy-25d0e1dd220d
        # TODO:  ANOVA: https://www.statsmodels.org/dev/examples/notebooks/generated/interactions_anova.html

        # -----------------------LOG-LINEAR----------------------------------------

        def log_func(x):
            if not x:
                return 0
            else:
                x = np.log(x)
            return x

        merged_res_dur['seconds'] = merged_res_dur['seconds'].apply(log_func)
        y, X_log = dmatrices('value~seconds', data=merged_res_dur, return_type='dataframe')
        mod_log = sm.OLS(y, X_log)  # Describe model
        res_log = mod_log.fit()  # Fit model
        context["statistics_extended_log"] = res_log.summary()

        r_squared_log = res_log.rsquared
        context["r_squared_log"] = r_squared_log
        r_squared_log_adj = res_log.rsquared_adj
        context["r_squared_log_adj"] = r_squared_log_adj
        #

        # --------Log seconds and mean values for graph

        deviation_df = pd.DataFrame(deviation_array)
        deviation_df['mean_rows'] = deviation_df.mean(axis=1)
        deviation_df.reset_index(inplace=True)
        deviation_df['duration'] = deviation_df['duration'].apply(log_func)
        deviation_mean_df = deviation_df[['duration', 'mean_rows']].values

        dev_log_data = []
        for row in deviation_mean_df:
            dev_log_data.append([row[0], row[1]])

        context["log_data"] = dev_log_data

        # -------Calculate Regression equation - lin log
        # y = a + b*ln(x)
        # -- Reshape Dataframe into 1D-Array for calculations
        vars = ['seconds']
        X_log = X_log[vars]

        X_log_a = np.array(X_log)
        X_log_1D = X_log_a.ravel()
        y_a = np.array(y)
        y_1D = y_a.ravel()

        # --Calcualting equation
        eq_model_log = np.polyfit(X_log_1D, y_1D, 1)
        context["eq_model_log"] = str(
            "y = " + str(round(eq_model_log[0], 5)) + " * log(x) + " + str(round(eq_model_log[1], 5)))

        #############################Overall statistical tests for the datatable ###########################
        # Rainbow test for linearity (the null hypothesis is that the relationship is properly modelled as linear);
        # first number is an F-statistic and that the second is the p-value.

        rainbow_test = sm.stats.linear_rainbow(res)
        context["rainbow_f"] = rainbow_test[0]
        context["rainbow_p"] = rainbow_test[1]

        # print(rainbow_test)

        # Test assumed normal or exponential distribution using Lilliefors’ test.        #
        # Lilliefors’ test is a Kolmogorov - Smirnov test with estimated parameters.
        # first number: ksstatfloat Kolmogorov - Smirnov test  statistic with estimated mean and variance.
        # second number: pvaluefloat   If  the pvalue is lower  than some threshold, e.g. 0.05, then  we can  reject the   Null hypothesis  that  the  sample comes from a normal distribution.

        ks = sm.stats.diagnostic.kstest_normal(y, dist='norm', pvalmethod='table')
        context["ksstat"] = ks[0]
        ksstat_p = ks[1]
        context["ksstat_p"] = ks[1]
        # TODO. Provide explanation
        # kurtosistest only valid for n>=20

        # ------------------------Absolute

        x1_abs = sm.add_constant(
            x1_abs)  # add a row of ones as constant #TODO: Is this line necessary ? - https://365datascience.com/tutorials/python-tutorials/linear-regression/
        model = sm.OLS(y_abs, x1_abs)
        results_abs = model.fit()  # OLS = Ordinary Least Squares
        context["statistics_extended_abs_lin"] = results_abs.summary()

        # -------------------------Extract single parameters from summary - linear regression
        b0_abs_lin = results_abs.params[0]  # constant coefficient / Intercept
        b1_abs_lin = results_abs.params[1]  # seconds coefficient / Slope
        print(results_abs.f_pvalue)
        b0_r_abs_lin = round(b0_abs_lin, 5)
        context["intercept_abs_lin"] = b0_r_abs_lin
        b1_r_abs_lin = round(b1_abs_lin, 5)
        context["slope_abs_lin"] = b1_r_abs_lin
        context["reg_eq_abs_lin"] = (
                "y = " + str(b0_r_abs_lin) + " + x1 * " + str(b1_r_abs_lin)
        )

        # --------------------------relative

        x_rel = sm.add_constant(x1_rel)  # add a row of ones as constant
        model = sm.OLS(y_rel, x_rel)
        results_rel = model.fit()  # OLS = Ordinary Least Squares

        # -------------------------Extract single parameters from summary - linear regression
        b0_rel_lin = results_rel.params[0]  # constant coefficient / Intercept
        b1_rel_lin = results_rel.params[1]  # seconds coefficient / Slope
        b0_r_rel_lin = round(b0_rel_lin, 5)
        context["intercept_rel_lin"] = b0_r_rel_lin
        b1_r_rel_lin = round(b1_rel_lin, 5)
        context["slope_rel_lin"] = b1_r_rel_lin
        context["reg_eq_rel_lin"] = (
                "y = " + str(b0_r_rel_lin) + " + x1 * " + str(b1_r_rel_lin)
        )

        ######################################INTERPRETATION ################################################

        # --------------------------Calculate best fitting model

        r_sq_list = [r_squared_lin, r_squared_log, r_squared_poly2, r_squared_poly3]
        best_fit = max(r_sq_list)
        context["best_fit"] = str(str(round(best_fit * 100, 2)) + " %")

        def best_fit_model() -> str:
            if r_squared_lin == best_fit:
                return 'Linear Regression Model'
            elif r_squared_log == best_fit:
                return 'Logarithmic regression model'
            elif r_squared_poly2 == best_fit:
                return 'Polynomial Regression Model 2° degree'
            else:
                return 'Polynomial Regression Model 3° degree'

        context["best_fit_model"] = best_fit_model()

        context["interpretation_1"] = 'Under these conditions, a ' + str(
            parameter.values('parameter__name')[0]['parameter__name']) + ' magnitude increase/decrease of ' + str(
            round(res.params[1] * 3600, 3)) + ' ' + str(
            parameter.values('parameter__unit')[0]['parameter__unit']) + ' per hour is expected'

        context["interpretation_2"] = '1 hour of sample storage under the tested conditions causes the the ' + str(
            parameter.values('parameter__name')[0]['parameter__name']) + ' level to change by ' + str(
            round(res.params[1] * 3600, 3)) + ' ' + str(parameter.values('parameter__unit')[0]['parameter__unit'])

        # print(res.params[1])

        # -------------------------- Normal distribution

        def distrib() -> str:
            if ksstat_p <= 0.05:
                return 'The data IS NOT normally distributed. KS-p-value: ' + str(
                    round(ksstat_p, 4)) + ' (only valid if n > 20)'
            else:
                return 'The data IS normally distributed. KS-p-value: ' + str(
                    round(ksstat_p, 4)) + ' (only valid if n > 20)'

        context["interpretation_dist"] = distrib()

        ###################################  Power Analysis #########################################

        #  ---------------- power analysis - linear regression
        effect_lin = r_squared_lin
        effect_log = r_squared_log
        alpha = 0.05
        nobs = Subject.objects.filter(settings__in=[self.object]).count()

        # perform power analysis
        analysis = TTestIndPower()
        power_lin = analysis.solve_power(effect_lin, power=None, nobs1=nobs, ratio=1.0, alpha=alpha)
        power_log = analysis.solve_power(effect_log, power=None, nobs1=nobs, ratio=1.0, alpha=alpha)

        context["power_lin"] = round(power_lin, 2)
        context["power_log"] = round(power_log, 2)

        power_lin_est = []
        for lin_est in range(1, 10):
            lin_est = lin_est / 10
            # print(lin_est)
            nobs = analysis.solve_power(effect_lin, power=lin_est, nobs1=None, ratio=1.0, alpha=alpha)
            data_for_graph = (nobs, lin_est)
            power_lin_est.append(data_for_graph)
        context['power_lin_est'] = power_lin_est

        # power = TTestIndPower().solve_power(effect_size=effect_size,
        #                                     nobs1=nobs1,
        #                                     ratio=ratio,
        #                                     power=None,
        #                                     alpha=alpha,
        #                                     alternative='two-sided')

        # ---------------------Image for Power estimation
        # -----------------------Render with <img src="data:image/png,base64,{{ power|safe }}" alt="">
        # nobs = Subject.objects.filter(settings__in=[self.object]).count()
        # print(nobs)
        # panalysis = TTestIndPower()
        #
        # def powerFigure():
        #     panalysis.plot_power(
        #         dep_var="nobs",
        #         nobs=np.arange(5, nobs),
        #         effect_size=np.arange(0.5, 1.5, .2),
        #         alpha=0.05,
        #         ax=None,
        #         title='Power-analysis',
        #
        #     )
        #     plt.xlabel('Number of subjects', fontsize=20)
        #     plt.ylabel('Power', fontsize=20)
        #     plt.show()
        #
        # context['power'] = panalysis
        # context['panalysis'] = panalysis

        ############################### Calculate maximum permissible error (MPE)##########################

        cv_g = ParameterUser.objects.filter(setting=self.object).values('parameter__cv_g')[0]['parameter__cv_g']
        cv_i = ParameterUser.objects.filter(setting=self.object).values('parameter__cv_i')[0]['parameter__cv_i']
        cv_a = ParameterUser.objects.filter(setting=self.object).values('cv_a')[0]['cv_a']
        context['cv_g']= cv_g
        context['cv_i']= cv_i
        context['cv_a']= cv_a
        rcv = 2 ** 0.5 * (1.96 * (cv_a ** 2 + cv_i ** 2) ** 0.5)
        context['rcv']= round(rcv, 2)
        allow_dev=0.5*cv_i
        context['allow_dev']=round(allow_dev, 2)
        accept_dev=0.7*allow_dev
        context['accept_dev'] =round(accept_dev, 2)
        allow_bias=0.25*math.sqrt(cv_i**2 + cv_g**2)
        context['allow_bias'] =round(allow_bias, 2)

        ###################################  Data import / export ####################################

        # ---------------------------Import
        # def upload_stability_data(request):
        #     if request.method == "POST":
        #         form = UploadExcelForm(request.POST, request.FILES)
        #         if form.is_valid():
        #             kappa = request.FILES['file']
        #             # Do work on kappa/excel file here with Pandas
        #             output = io.BytesIO()
        #             writer = pd.ExcelWriter(output, engine='xlsxwriter')
        #             kappa.to_excel(writer, index=False)
        #             writer.save()
        #             output.seek(0)
        #             response = HttpResponse(output,
        #                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        #         response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % 'Download'
        #         return response
        #     else:
        #         form = UploadExcelForm()
        #
        #     return render(request, 'calculator/upload_form.html', {'form': form})

        # -----------------------------Export

        # https://stackoverflow.com/questions/35267585/django-pandas-to-http-response-download-file
        # https://djangoadventures.com/how-to-create-file-download-links-in-django/
        #

        MDATA = datetime.now().strftime('%Y-%m-%d')

        def data_export_xlsx(pk):
            data = merged_res_dur
            slug = parameter.values('name')[0]['name']

            df = pd.DataFrame(merged_res_dur)
            # Convertendo data para o formato correto
            # df['dataset__created'] = df['dataset__created'].apply(
            #     lambda x: x.strftime('%Y-%m-%d %H:%M'))
            # df['dataset__modified'] = df['dataset__modified'].apply(
            #     lambda x: x.strftime('%Y-%m-%d %H:%M'))

            filename = f'stability_data_{slug}_{MDATA}.xlsx'

            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.xlsx') as tmp:
                df.to_excel(tmp.name, sheet_name=f'stability_data_{slug}')
                tmp.flush()
                tmp.seek(0)
                data = tmp.read()
            return (data, filename)

        # context["export_data_excel"] = data_export_xlsx(id(self))

        # --------------------MatPlotLib Scattergramm:
        # plt.scatter(x1_rel, y_rel)
        # plt.xlabel('Seconds', fontsize=20)
        # plt.ylabel('Results', fontsize=20)
        # plt.show()

        # ------------------------Return context

        context.update(
            {
                "subjects": subjects,
                "results": results,
                "durations": Duration.objects.all(),
                "r_square": results_abs.rsquared,
                "f_p_value": results_abs.f_pvalue,
                "f_p_value_perc": results_abs.f_pvalue * 100,
                "f_value": results_abs.fvalue,
                "f_p_log_value": res_log.f_pvalue,
                "f_p_log_value_perc": res_log.f_pvalue * 100,
                # Essentially, it asks, is this a useful variable? Does it help us explain the variability we have in this case?
            }
        )
        return context


from io import BytesIO
from openpyxl import Workbook  # Documentation at https://openpyxl.readthedocs.io/en/stable/tutorial.html
from openpyxl.cell import cell
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font

def DownloadExcel(request, setting_pk):
    excelfile = BytesIO()
    workbook = Workbook()
    workbook.remove(workbook.active)
    owner = request.user
    setting = Setting.objects.get(pk=setting_pk, owner=owner)
    results = setting.results.all()
    print(results)
    ws1 = workbook.create_sheet(title="Basic Information")
    ws1.sheet_view.showGridLines = False

    now = timezone.now().strftime('%d-%m-%Y - %H-%M')


    ws1['A1'] = "EFLM Stability Calculator"
    ws1['A1'].font = Font(size=25, color="e63946", bold=True)
    ws1['A2'] = "EFLM Working Group Preanalytical Phase (WG-PRE)"
    ws1['A2'].font = Font(size=20, color="e63946")
    ws1['A4'] = 'Downloaded by ' + request.user.user_name + ' on ' + now
    ws1['A4'].font = Font(italic=True)
    ws1['A6'] = "Stability study setting details"
    ws1['A7'] = "Name"
    ws1['B7'] = str(setting.name)
    ws1['A8'] = "Parameter"
    ws1['B8'] = str(setting.parameter)
    ws1['A9'] = "Samples"
    ws1['B9'] = str(setting.sample)
    ws1['A10'] = "Source of samples"
    ws1['B10'] = setting.sample_type
    ws1['A11'] = "Storage Condition"
    ws1['B11'] = str(setting.condition)
    ws1['A12'] = "Type of study design"
    ws1['B12'] = str(setting.design_type)
    ws1['A13'] = "Primary samples or aliquots"
    ws1['B13'] = str(setting.design_sample)
    ws1['A14'] = "Freeze thaw cycles (n)"
    ws1['B14'] = str(setting.freeze_thaw_cycles)
    ws1['A15'] = "Protocol"
    ws1['B15'] = str(setting.protocol)
    ws1['A16'] = "Comment"
    ws1['B16'] = str(setting.comment)




   # -------------sheet 2 - data ------------------

    ws2 = workbook.create_sheet('Data')
    # for subject in setting.subjects.all():
    #     ws2.append([str(subject)])
    #     for duration in setting.durations.all():
    #         ws2.append([str(duration)])
    #         for result in setting.durations.
    ws2["A1"] = 'Subject'
    ws2["B1"] = 'Storage duration'
    ws2["C1"] = 'Result'
    ws2["D1"] = 'Unit'

    for count, result in enumerate(results):
        ws2.cell(row=count+2, column=1).value = str(result.subject)
        ws2.cell(row=count+2, column=2).value = str(result.duration)
        ws2.cell(row=count+2, column=3).value = result.value
        ws2.cell(row=count+2, column=4).value = str(result.setting.parameter.parameter.unit)

    # -------------sheet 3 - statistics ------------------

    ws3 = workbook.create_sheet('Statistics')

    ws3['A1'] = 'Descriptive statistics'
    ws3['A2'] = 'Number of Subjects'
    ws3['B2'] = Subject.objects.filter(settings__in=[setting]).count()
    ws3['A3'] = 'Number of tested storage durations'
    ws3['B3'] = Duration.objects.filter(settings__in=[setting]).count()
    ws3['A4'] = 'Number of results '
    ws3['B4'] = Result.objects.filter(setting=setting).count()

    for count, duration in enumerate(setting.durations.all()):
        ws3.cell(row=6, column=count+2).value = str(duration)

    ws3['A7'] = 'Average'
    ws3['A8'] = 'Standard deviation'
    ws3['A9'] = 'Coefficient of Variation (%)'
    ws3['A10'] = 'Deviation from baseline (%)'
    for count, duration in enumerate(setting.durations.all()):
        ws3.cell(row=7, column=count+2).value = setting.average_tot(duration=duration)





    workbook.save(excelfile)

    response = HttpResponse(excelfile.getvalue(), content_type='application/')
    response['Content-Disposition'] = f'attachment; filename=stability-study-data-{setting.name}-{now}.xlsx'
    return response


def upload_view(request):
    form = UploadExcelForm
    return render(request, 'calculator/upload_form.html', {"form": form})


# --------------------------------------INSTRUMENT-----------------------------------------


def instrument_list(request):
    form = InstrumentForm(request.POST or None)
    instruments = Instrument.objects.all()

    if request.method == 'POST':
        if form.is_valid():

            name = form.cleaned_data["name"]
            manufacturer = form.cleaned_data['manufacturer']
            instrument = Instrument(name=name, manufacturer=manufacturer)
            owner = request.user
            instrument.owner = owner
            instrument.save()
            return redirect('instrument-detail', pk=instrument.id)
        else:
            return render(request, 'calculator/partials/instrument_form.html', context={
                'form': form
            })

    context = {
        'form': form,
        'instruments': instruments,
    }

    return render(request, 'calculator/instrument_list.html', context)


def add_instrument_form(request):
    form = InstrumentForm()
    context = {
        "form": form
    }
    return render(request, 'calculator/partials/instrument_form.html', context)


def instrument_detail(request, pk):
    # instrument = Instrument.objects.get(pk=pk)
    instrument = get_object_or_404(Instrument, pk=pk)
    if not instrument.owner == request.user:
        return HttpResponseForbidden
    else:
        context = {
            "instrument": instrument
        }
        return render(request, 'calculator/partials/instrument_detail.html', context)


def edit_instrument(request, pk):
    instrument = Instrument.objects.get(pk=pk)
    form = InstrumentForm(request.POST or None, instance=instrument)

    # This part is so that the update does not produce more objects
    if request.method == 'POST':
        if form.is_valid():
            instrument = form.save()
            return redirect('instrument-detail', pk=instrument.id)

    context = {
        "form": form,
        "instrument": instrument,
    }
    return render(request, 'calculator/partials/instrument_form.html', context)


def delete_instrument(request, pk):
    instrument = Instrument.objects.get(pk=pk)
    instrument.delete()
    return HttpResponse('')


# ------------------------------------PARAMETER---------------------------------------


def parameter_list(request):
    form = ParameterUserForm(request.POST or None, user=request.user)
    parameters = ParameterUser.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            parameter = form.save(commit=False)
            parameter.owner = request.user
            parameter.save()
            return redirect('parameter-detail', pk=parameter.id)
        else:
            context = {
                'form': form,
                'parameters': ParameterUser.objects.filter()
            }
            return render(request, 'calculator/partials/parameter_form.html', context)

    context = {
        'form': form,
        'parameters': parameters,

    }

    return render(request, 'calculator/parameter_list.html', context)


def search_parameter(request):
    if 'name' in request.POST:
        try:
            parameters = Parameter.objects.filter(name__icontains=request.POST.get("name"))
        except Parameter.DoesNotExist:
            parameters = None

    context = {
        "parameters": parameters,

    }
    return render(request, 'calculator/partials/parameter_searchresult.html', context)


def select_parameter(request, pk):
    parameter = Parameter.objects.get(pk=pk)
    initial_dict = {
        'parameter': parameter.id
    }
    form = ParameterUserForm(
        user=request.user,
        initial=initial_dict
    )

    # form.initial['parameter'].id = parameter.id

    context = {
        "form": form,
        "parameter_name": parameter.name,
        "parameter_unit": parameter.unit,
        "parameter_cvg": parameter.cv_g,
        "parameter_cvi": parameter.cv_i,
    }

    return render(request, 'calculator/partials/parameter_form.html', context)


def add_parameter_form(request):
    # try:
    #     parameter = Parameter.objects.get(name=request.POST.get("name"))
    # except Parameter.DoesNotExist:
    #     parameter = None
    form = ParameterUserForm(user=request.user)
    parameter_select = Parameter.objects.all()
    # form = ParameterUserForm(user=request.user)

    context = {
        "form": form,
        "parameter_list": parameter_select
    }

    return render(request, 'calculator/partials/parameter_form.html', context)


def parameter_detail(request, pk):
    parameter_user = get_object_or_404(ParameterUser, pk=pk)
    if not parameter_user.owner == request.user:
        return HttpResponseForbidden
    else:
        context = {
            "parameter": parameter_user
        }
        return render(request, 'calculator/partials/parameter_detail.html', context)


def edit_parameter(request, pk):
    parameter = ParameterUser.objects.get(pk=pk)
    form = ParameterUserForm(request.POST or None, instance=parameter, user=request.user)

    # This part is so that the update does not produce more objects
    if request.method == 'POST':
        if form.is_valid():
            parameter = form.save()
            return redirect('parameter-detail', pk=parameter.id)

    context = {
        "form": form,
        "parameter": parameter,
        "parameter_name": parameter.parameter.name,
        "parameter_unit": parameter.parameter.unit,
        "parameter_cvg": parameter.parameter.cv_g,
        "parameter_cvi": parameter.parameter.cv_i,
    }
    return render(request, 'calculator/partials/parameter_form.html', context)


def delete_parameter(request, pk):
    parameter = ParameterUser.objects.get(pk=pk)
    parameter.delete()
    return HttpResponse('')


# --------------------------------------PREANALYTICS----------------------------------------

def preanalytical_set_list(request):
    form = PreanalyticalSetForm(request.POST)
    preanalytical_sets = PreanalyticalSet.objects.all()
    if request.method == 'POST':
        if form.is_valid():
            preanalytical_set = form.save(commit=False)
            preanalytical_set.owner = request.user
            preanalytical_set.save()
            return redirect('preanalytical-set-detail', pk=preanalytical_set.id)
        else:
            context = {
                'form': form,
                'preanalytical_sets': PreanalyticalSet.objects.all()
            }
            return render(request, 'calculator/partials/preanalytical_set_form.html', context)

    context = {
        'form': form,
        'preanalytical_sets': preanalytical_sets,

    }

    return render(request, 'calculator/preanalytical_set_list.html', context)


def add_preanalytics_form(request):
    form = PreanalyticalSetForm()
    context = {
        "form": form
    }
    return render(request, 'calculator/partials/preanalytical_set_form.html', context)


def preanalytics_detail(request, pk):
    preanalytical_set = get_object_or_404(PreanalyticalSet, pk=pk)
    if not preanalytical_set.owner == request.user:
        return HttpResponseForbidden
    else:
        context = {
            "preanalytical_set": preanalytical_set
        }
        return render(request, 'calculator/partials/preanalytical_set_detail.html', context)


def edit_preanalytical_set(request, pk):
    preanalytical_set = PreanalyticalSet.objects.get(pk=pk)
    form = PreanalyticalSetForm(request.POST or None, instance=preanalytical_set)

    # This part is so that the update does not produce more objects
    if request.method == 'POST':
        if form.is_valid():
            preanalytical_set = form.save()
            return redirect('preanalytical-set-detail', pk=preanalytical_set.id)

    context = {
        "form": form,
        "preanalytical_set": preanalytical_set,
    }
    return render(request, 'calculator/partials/preanalytical_set_form.html', context)


def delete_preanalytical_set(request, pk):
    preanalytical_set = PreanalyticalSet.objects.get(pk=pk)
    preanalytical_set.delete()
    return HttpResponse('')


# --------------------------------------SAMPLE----------------------------------------

def sample_list(request):
    form = SampleForm(request.POST)
    samples = Sample.objects.all()
    if request.method == 'POST':
        if form.is_valid():
            sample = form.save(commit=False)
            sample.owner = request.user
            sample.save()
            return redirect('sample-detail', pk=sample.id)
        else:
            context = {
                'form': form,
                'samples': Sample.objects.all()
            }
            return render(request, 'calculator/partials/sample_form.html', context)

    context = {
        'form': form,
        'samples': samples,

    }

    return render(request, 'calculator/sample_list.html', context)


def add_sample_form(request):
    form = SampleForm()
    context = {
        "form": form
    }
    return render(request, 'calculator/partials/sample_form.html', context)


def sample_detail(request, pk):
    sample = get_object_or_404(Sample, pk=pk)
    if not sample.owner == request.user:
        return HttpResponseForbidden
    else:
        context = {
            "sample": sample
        }
        return render(request, 'calculator/partials/sample_detail.html', context)


def edit_sample(request, pk):
    sample = Sample.objects.get(pk=pk)
    form = SampleForm(request.POST or None, instance=sample)

    # This part is so that the update does not produce more objects
    if request.method == 'POST':
        if form.is_valid():
            sample = form.save()
            return redirect('sample-detail', pk=sample.id)

    context = {
        "form": form,
        "sample": sample,
    }
    return render(request, 'calculator/partials/sample_form.html', context)


def delete_sample(request, pk):
    sample = Sample.objects.get(pk=pk)
    sample.delete()
    return HttpResponse('')


# -------------------------------------SETTING----------------------------------------

def setting_list(request):
    form = SettingForm(request.POST or None, user=request.user)
    settings = Setting.objects.filter()
    if request.method == 'POST':
        if form.is_valid():
            setting = form.save(commit=False)
            setting.owner = request.user
            setting.save()
            form.save_m2m()
            return redirect('setting-detail', pk=setting.id)
        else:
            context = {
                'form': form,
                'settings': settings
            }
            return render(request, 'calculator/partials/setting_form.html', context)

    context = {
        'form': form,
        'settings': settings

    }

    return render(request, 'calculator/setting_list.html', context)


def add_setting_form(request):
    form = SettingForm(user=request.user)
    owner = request.user

    context = {
        "form": form,
        "owner": owner,

    }
    return render(request, 'calculator/partials/setting_form.html', context)


def setting_detail(request, pk):
    setting = get_object_or_404(Setting, pk=pk)
    if not setting.owner == request.user:
        return HttpResponseForbidden
    else:
        context = {
            "setting": setting,
        }
        return render(request, 'calculator/partials/setting_detail.html', context)


def edit_setting(request, pk):
    setting = Setting.objects.get(pk=pk)
    form = SettingForm(request.POST or None, instance=setting, user=request.user)

    # This part is so that the update does not produce more objects
    if request.method == 'POST':
        if form.is_valid():
            setting = form.save()
            return redirect('setting-detail', pk=setting.id)

    context = {
        "form": form,
        "setting": setting,
    }
    return render(request, 'calculator/partials/setting_form.html', context)


def delete_setting(request, pk):
    setting = Setting.objects.get(pk=pk)
    setting.delete()
    return HttpResponse('')


# -------------------------------------CONDITION----------------------------------------

def condition_list(request):
    form = ConditionForm(request.POST or None)
    conditions = Condition.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            condition = form.save(commit=False)
            condition.owner = request.user
            condition.save()
            return redirect('condition-detail', pk=condition.id)
        else:
            context = {
                'form': form,
                'conditions': Condition.objects.all()
            }
            return render(request, 'calculator/partials/condition_form.html', context)

    context = {
        'form': form,
        'conditions': conditions,

    }

    return render(request, 'calculator/condition_list.html', context)


def add_condition_form(request):
    form = ConditionForm()
    context = {
        "form": form
    }
    return render(request, 'calculator/partials/condition_form.html', context)


def condition_detail(request, pk):
    condition = get_object_or_404(Condition, pk=pk)
    if not condition.owner == request.user:
        return HttpResponseForbidden
    else:
        context = {
            "condition": condition
        }
        return render(request, 'calculator/partials/condition_detail.html', context)


def edit_condition(request, pk):
    condition = Condition.objects.get(pk=pk)
    form = ConditionForm(request.POST or None, instance=condition)

    # This part is so that the update does not produce more objects
    if request.method == 'POST':
        if form.is_valid():
            condition = form.save()
            return redirect('condition-detail', pk=condition.id)

    context = {
        "form": form,
        "condition": condition,
    }
    return render(request, 'calculator/partials/condition_form.html', context)


def delete_condition(request, pk):
    condition = Condition.objects.get(pk=pk)
    condition.delete()
    return HttpResponse('')


# -------------------------------------DURATION----------------------------------------

def duration_list(request):
    form = DurationForm(request.POST or None)
    durations = Duration.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            duration = form.save(commit=False)
            duration.owner = request.user
            duration.save()
            return redirect('duration-detail', pk=duration.id)
        else:
            context = {
                'form': form,
                'durations': Duration.objects.all()
            }
            return render(request, 'calculator/partials/duration_form.html', context)

    context = {
        'form': form,
        'durations': durations,
    }

    return render(request, 'calculator/duration_list.html', context)


def add_duration_form(request):
    form = DurationForm()
    context = {
        "form": form
    }
    return render(request, 'calculator/partials/duration_form.html', context)


def duration_detail(request, pk):
    duration = get_object_or_404(Duration, pk=pk)
    if not duration.owner == request.user:
        return HttpResponseForbidden
    else:
        context = {
            "duration": duration
        }
        return render(request, 'calculator/partials/duration_detail.html', context)


def edit_duration(request, pk):
    duration = Duration.objects.get(pk=pk)
    form = DurationForm(request.POST or None, instance=duration)

    # This part is so that the update does not produce more objects
    if request.method == 'POST':
        if form.is_valid():
            duration = form.save()
            return redirect('duration-detail', pk=duration.id)

    context = {
        "form": form,
        "duration": duration,
    }
    return render(request, 'calculator/partials/duration_form.html', context)


def delete_duration(request, pk):
    duration = Duration.objects.get(pk=pk)
    duration.delete()
    return HttpResponse('')


# -------------------------------------RESULTS---------------------------------

# def create_result(request, setting_pk):
#     setting = Setting.objects.get(pk=setting_pk)
#     durations = Duration.objects.filter(setting=setting)
#     subjects = Subject.objects.filter(setting=setting)
#     results = Result.objects.filter(setting=setting)
#
#     ResultFormSet = modelformset_factory(Result, fields=('value', 'setting', 'duration', 'subject'),
#                                          extra=1)
#
#     if request.method == 'POST':
#         formset = ResultFormSet(request.POST or None)
#
#         if formset.is_valid():
#
#             results = formset.save()
#             # TODO: Show success message after save that fades automatically: https://stackoverflow.com/questions/61153261/make-success-message-disappear-after-few-seconds-of-django-form-submission-and-d
#             # messages.add_message(request, messages.SUCCESS, 'Entry saved')
#             # for result in results:
#             #     sid=result.setting.id
#             # # return redirect('result-detail', pk=rid)
#             # return redirect('create-result', setting_pk=sid)
#
#         else:
#             context = {
#                 'formset': formset,
#                 'results': results
#             }
#             return render(request, 'calculator/partials/result_form.html', context)
#     formset = ResultFormSet(queryset=Result.objects.none())
#
#     context = {
#         'formset': formset,
#         'durations': durations,
#         'setting': setting,
#         'subjects': subjects,
#         'results': results,
#     }
#
#     return render(request, 'calculator/result_list.html', context)
def result_list(request, setting_pk):
    setting = Setting.objects.get(pk=setting_pk)
    durations = Duration.objects.filter(settings__in=[setting])
    subjects = Subject.objects.filter(settings__in=[setting])
    results = Result.objects.filter(setting=setting)
    form = ResultForm(subjects, durations, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            # https://zerotobyte.com/using-django-bulk-create-and-bulk-update/
            # https://stackoverflow.com/questions/53594745/what-is-the-use-of-cleaned-data-in-django
            # subject = Result.subject.through(for subject in subjects: return subject.id)
            result_list = []
            for key, value in form.cleaned_data.items():
                if not value:
                    continue
                # print(key, value)
                items = key.split("-")
                subject_id = items[1]
                duration = Duration.objects.get(pk=items[2])
                result = Result(value=value, setting=setting, duration=duration, subject_id=subject_id)
                result.owner = request.user
                result_list.append(result)

            Result.objects.bulk_create(result_list)

            # result = form.save(commit=False)
            # result.setting = setting
            # result.duration = duration
            # # result.subjects.add(subject)
            # # FIXME: Define current subject for asignment
            # result.save()
            # return redirect('result-detail', pk=subject.result.id)
            # return redirect('result-detail')
            form = ResultForm(subjects, durations, data=None)

        else:
            context = {
                'form': form,
                'results': results
            }
            return render(request, 'calculator/partials/result_form.html', context)

    context = {
        "form": form,
        'durations': durations,
        'setting': setting,
        'subjects': subjects,
        'results': results,
    }

    return render(request, 'calculator/result_list.html', context)


def add_result_form(request, setting_pk, duration_pk):
    form = ResultForm()
    # duration = Duration.objects.get(pk=duration_pk)
    subjects = Subject.objects.filter(settings__in=[setting_pk], result__duration_id=duration_pk)

    context = {
        "form": form,
        "subjects": subjects,
        # "duration": duration
    }
    return render(request, 'calculator/partials/result_form.html', context)


# def add_result_form(request):
#     form = ResultForm()
#     context = {
#         "form": form
#     }
#     return render(request, 'calculator/partials/result_form.html', context)


def result_detail(request, pk):
    result = get_object_or_404(Result, pk=pk)
    if not result.owner == request.user:
        return HttpResponseForbidden
    else:
        context = {
            "result": result,
            # "duration": duration,
        }
        return render(request, 'calculator/partials/result_detail.html', context)


def edit_result(request, pk):
    result = Result.objects.get(pk=pk)
    form = ResultForm(request.POST or None, instance=result)

    # This part is so that the update does not produce more objects
    if request.method == 'POST':
        if form.is_valid():
            result = form.save()
            return redirect('result-detail', pk=result.id)

    context = {
        "form": form,
        "result": result,
    }
    return render(request, 'calculator/partials/result_form.html', context)


# def edit_result(request, pk):
#     result = Result.objects.get(pk=pk)
#     form = ResultForm(request.POST or None, instance=result)
#
#     # This part is so that the update does not produce more objects
#     if request.method == 'POST':
#         if form.is_valid():
#             result = form.save()
#             return redirect('result-detail', pk=result.id)
#
#     context = {
#         "form": form,
#         "result": result,
#     }
#     return render(request, 'calculator/partials/result_form.html', context)


def delete_result(request, pk):
    result = Result.objects.get(pk=pk)
    result.delete()
    return HttpResponse('')


# -------------------------------------SUBJECT----------------------------------------

def subject_list(request):
    form = SubjectForm(request.POST or None)
    subjects = Subject.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            subject = form.save(commit=False)
            subject.owner = request.user
            subject.save()
            return redirect('subject-detail', pk=subject.id)
        else:
            context = {
                'form': form,
                'subjects': Subject.objects.all()
            }
            return render(request, 'calculator/partials/subject_form.html', context)

    context = {
        'form': form,
        'subjects': subjects,
    }

    return render(request, 'calculator/subject_list.html', context)


def add_subject_form(request):
    form = SubjectForm()
    context = {
        "form": form,

    }
    return render(request, 'calculator/partials/subject_form.html', context)


def subject_detail(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if not subject.owner == request.user:
        return HttpResponseForbidden
    else:
        context = {
            "subject": subject
        }
        return render(request, 'calculator/partials/subject_detail.html', context)


def edit_subject(request, pk):
    subject = Subject.objects.get(pk=pk)
    form = SubjectForm(request.POST or None, instance=subject)

    # This part is so that the update does not produce more objects
    if request.method == 'POST':
        if form.is_valid():
            subject = form.save()
            return redirect('subject-detail', pk=subject.id)

    context = {
        "form": form,
        "subject": subject,
    }
    return render(request, 'calculator/partials/subject_form.html', context)


def delete_subject(request, pk):
    subject = Subject.objects.get(pk=pk)
    subject.delete()
    return HttpResponse('')


def item_lists(request):
    settings = Setting.objects.all()
    parameters = Parameter.objects.all()
    subjects = Subject.objects.all()
    durations = Duration.objects.all()
    samples = Sample.objects.all()
    conditions = Condition.objects.all()
    instruments = Instrument.objects.all()

    context = {
        'settings': settings,
        'parameters': parameters,
        'subjects': subjects,
        'durations': durations,
        'samples': samples,
        'conditions': conditions,
        'instruments': instruments,
    }
    return render(request, 'itemlists.html', context)


def new_parameter(request):
    form = NewParameterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            parameter_request = form.save(commit=False)
            parameter_request.user = request.user
            parameter_request.user.email = request.user.email
            parameter_request.save()
            return render(request, 'calculator/thankyou.html')
        else:
            context = {
                'form': form,
        }
        return render(request, 'calculator/newparameter.html', context)

        # try:
        #     send_mail(subject, message, from_email, ['admin@example.com'])
        # except BadHeaderError:
        #     return HttpResponse('Invalid header found.')
        # return redirect('success')
    return render(request, "calculator/newparameter.html", {'form': form})

def thankyou_mail(request):
    return HttpResponse('Thank you for your message.')