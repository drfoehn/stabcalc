from django.shortcuts import render
from django.views.generic import ListView, DetailView
from database.models import *
from database.forms import *
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from .filters import AnalyteFilter

class AnalyteSpecimenIndex(ListView):
    model = AnalyteSpecimen
    # paginate_by = 50

    # Reactivate to use with django-filter
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["analyte_filter"] = AnalyteFilter(self.request.GET, queryset=self.get_queryset())
    #     return context

    # def get_queryset(self):
    #     searchstring=self.request.GET.get('q',""),
    #     filters={'name__icontains':searchstring} if searchstring else {}
    #     return super().get_queryset().filter(**filters)



def search_analyte(request):
    search_text = request.GET.get('search', "")
    if search_text:
        results = AnalyteSpecimen.objects.filter(analyte__name__icontains=search_text).all().order_by('analyte')
        template = 'database/partials/analyte_searchresult.html'
    else:
        results = AnalyteSpecimen.objects.order_by('analyte')
        template = 'database/partials/search_list.html'
    context= {'results':results}
    return render(request, template, context)
# def search_analyte(request):
#     searchterm = request.GET.get('qs', None)
#     if searchterm:
#         searchresult = Analyte.objects.filter(name__icontains=searchterm).all()
#         template = 'database/partials/analyte_searchresult.html'
#     else:
#         searchresult = []
#         template = 'database/analyte_search.html'
#     return render(request=request,
#                   template_name=template,
#                   context={'searchresult':searchresult})




# def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     context['analyte_specimen'] = self.object.analyte_specimen.all()
#
#     graphs = {}
#     for analyte_specimen in context['analyte_specimen']:
#         graphs[analyte_specimen.id] = {}
#         for stability in analyte_specimen.stability.all():
#             if stability.eq_type:
#                 x_values = np.linspace(0, 100)
#                 if stability.eq_type == Stability.LIN:
#                     y_values = stability.b0 + stability.b1 * x_values
#                 elif stability.eq_type == Stability.QUADR:
#                     y_values = stability.b0 + stability.b1 * x_values + stability.b2 * x_values ** 2
#                 elif stability.eq_type == Stability.CUBIC:
#                     y_values = stability.b0 + stability.b1 * x_values + stability.b2 * x_values ** 2 + stability.b3 * x_values ** 3
#                 elif stability.eq_type == Stability.EXP:
#                     y_values = stability.exp_a * np.exp(stability.exp_b * x_values)
#                 else:
#                     raise ValueError("Invalid equation type")
#
#                 # Create the plot
#                 fig, ax = plt.subplots()
#                 ax.plot(x_values, y_values)
#                 # Save it to a BytesIO object
#                 buf = BytesIO()
#                 plt.savefig(buf, format='png')
#                 # Embed the result in the html output.
#                 data = base64.b64encode(buf.getbuffer()).decode("ascii")
#                 graphs[analyte_specimen.id][stability.id] = f"data:image/png;base64,{data}"
#
#     context['graphs'] = graphs
#     return context

class AnalyteSpecimenDetail(DetailView):
    model = Analyte

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # The related AnalyteSpecimen instances can be accessed via the related_name
        context['analyte_specimen'] = self.object.analyte_specimen.all()

        # Initialize the dictionary to store graphs.
        graphs = {}

        for analyte_specimen in context['analyte_specimen']:
            for stability in analyte_specimen.stability.all():
                if not stability.eq_type:
                    continue
                x_values = np.linspace(0, stability.max_time_evaluated)
                if stability.eq_type == Stability.LIN:
                    y_values = stability.b0 + stability.b1 * x_values
                elif stability.eq_type == Stability.QUADR:
                    y_values = stability.b0 + stability.b1 * x_values + stability.b2 * x_values ** 2
                elif stability.eq_type == Stability.CUBIC:
                    y_values = stability.b0 + stability.b1 * x_values + stability.b2 * x_values ** 2 + stability.b3 * x_values ** 3
                elif stability.eq_type == Stability.EXP:
                    y_values = stability.exp_a * np.exp(stability.exp_b * x_values)
                else:
                    raise ValueError("Invalid equation type")

                fig, ax = plt.subplots()
                ax.plot(x_values, y_values)
                ax.set_xlabel(stability.get_max_time_evaluated_unit_display())
                ax.set_ylabel('%Deviation')
                buf = BytesIO()
                plt.savefig(buf, format='png')
                data = base64.b64encode(buf.getbuffer()).decode("ascii")
                # Store each graph in the dictionary with its associated stability instance's id.
                graphs[stability.pk] = f"data:image/png;base64,{data}"

                    # Add the dictionary of graphs to the context.
                context['graph'] = graphs
        print(graphs)
        return context


# def search_analyte(request):
#     if 'name' in request.POST:
#         try:
#             analytes = Analyte.objects.filter(name__icontains=request.POST.get("name"))
#         except Analyte.DoesNotExist:
#             analytes = None
#
#     context = {
#         "analytes": analytes,
#
#     }
#     return render(request, 'database/partials/analyte_searchresult.html', context)


def select_analyte(request, pk):
    analyte = AnalyteSpecimen.objects.get(pk=pk)
    initial_dict = {
        'analyte': analyte.pk
    }
    form = AnalyteSpecimenSearchForm(
        initial=initial_dict
    )

    # form.initial['parameter'].id = parameter.id

    context = {
        "form": form,
        "analyte_name": f"{analyte.analyte.name} - {analyte.specimen.name}",
    }

    return render(request, 'database/templates/database/analytespecimen_form.html', context)

