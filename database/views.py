from django.shortcuts import render
from django.views.generic import ListView, DetailView
from database.models import *
from database.forms import *
from .filters import AnalyteFilter

class AnalyteIndex(ListView):
    model = Analyte
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["analyte_filter"] = AnalyteFilter(self.request.GET, queryset=self.get_queryset())
        return context

class AnalyteDetail(DetailView):
    model = Analyte

def search_analyte_form(request):
    form = AnalyteSearchForm
    analyte_select = Analyte.objects.all()

    context = {
        "form": form,
        "analyte_list": analyte_select
    }

    return render(request, 'database/analyte_form.html', context)

def search_analyte(request):
    if 'name' in request.POST:
        try:
            analytes = Analyte.objects.filter(name__icontains=request.POST.get("name"))
        except Analyte.DoesNotExist:
            analytes = None

    context = {
        "analytes": analytes,

    }
    return render(request, 'database/partials/analyte_searchresult.html', context)


def select_analyte(request, pk):
    analyte = Analyte.objects.get(pk=pk)
    initial_dict = {
        'analyte': analyte.analyte_id
    }
    form = AnalyteSearchForm(
        initial=initial_dict
    )

    # form.initial['parameter'].id = parameter.id

    context = {
        "form": form,
        "analyte_name": analyte.name,
    }

    return render(request, 'database/analyte_form.html', context)

