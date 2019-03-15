import openpyxl
from django.http import HttpResponse
from django.template import loader
from .models import Runlog
from .forms import TatForm, SearchForm
from .functions import tab_raw, tab_panels, tab_other


def index(request):
    # if either submit button is pressed, enter this loop, otherwise just display the index page
    if request.method == "POST":

        # if input is from search form
        if 'search_input' in request.POST:
            form = SearchForm(request.POST)
            if form.is_valid():
                # save input variables but don't commit to the database
                search = form.save(commit=False)
                # perform query based on input values
                runs = Runlog.objects.filter(
                    run_id__contains=search.run_id, 
                    experiment__contains=search.experiment,
                    samples__contains=search.samples,
                    pipeline__contains=search.pipeline,
                    ).order_by('-instrument_date')
                # return rendered results page
                template = loader.get_template('db/search.html')
                context = {
                    'form': form,
                    'runs': runs,
                    }
                return HttpResponse(template.render(context, request))

        # if input is from KPI form
        if 'tat_input' in request.POST:
            form = TatForm(request.POST)
            if form.is_valid():
                # save input dates but don't commit to the database
                dates = form.save(commit=False)
                # perform query based on input values
                runs = Runlog.objects.filter(instrument_date__range=(dates.start_date, dates.end_date)).order_by('instrument_date', 'experiment')
                # open empty excel workbook
                wb = openpyxl.Workbook()
                panels = ['BRCA', 'CRM', 'CRUK', 'NIPT', 'TAM', 'TruSightCancer', 'TruSightOne']
                # Fill in raw data tab, panels tab and others tab
                tab_other(wb, runs, panels)
                tab_panels(wb, runs, panels)
                tab_raw(wb, runs)
                # save and return workbook as response
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheet.sheet')
                output_name = 'attachment; filename="KPI_' + str(dates.start_date) + '_' + str(dates.end_date) + '.xlsx"'
                response['Content-Disposition'] = output_name
                wb.save(response)
                return response

    # if no data inputted, display index page with empty values
    else:
        tatform = TatForm()
        searchform = SearchForm()
        template = loader.get_template('db/index.html')
        context = {
            'tatform': tatform,
            'searchform': searchform
            }
        return HttpResponse(template.render(context, request))
