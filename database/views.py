from django.shortcuts import render
from django.views.generic import ListView, DetailView
from database.models import *
from database.forms import *
from .filters import AnalyteFilter

class AnalyteIndex(ListView):
    model = Analyte
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
        results = Analyte.objects.filter(name__icontains=search_text).all()
        template = 'database/partials/analyte_searchresult.html'
    else:
        results = Analyte.objects.all()
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


class AnalyteDetail(DetailView):
    model = Analyte



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

