from django.shortcuts import render
from django.views.generic import ListView, DetailView
from database.models import *
from database.forms import *

class AnalyteIndex(ListView):
    model = Analyte

class AnalyteDetail(DetailView):
    model = Analyte


def search_analyte_form(request):
    # try:
    #     analyte = Analyte.objects.get(name=request.POST.get("name"))
    # except Parameter.DoesNotExist:
    #     analyte = None
    form = AnalyteSearchForm()
    analyte_select = Analyte.objects.all()

    context = {
        "form": form,
        "analyte_list": analyte_select
    }

    return render(request, 'database/analyte_form.html', context)