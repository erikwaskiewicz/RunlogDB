import openpyxl
from django.http import HttpResponse
from django.template import loader
from .models import Runlog
from .forms import TatForm
from .functions import tab_raw, tab_panels, tab_other


def index(request):
    # if data inputted and is valid:
    if request.method == "POST":
        form = TatForm(request.POST)
        if form.is_valid():
            # Create queryset
            dates = form.save(commit=False)
            runs = Runlog.objects.filter(instrument_date__range=(dates.start_date, dates.end_date)).order_by('-instrument_date')
            # open empty excel workbook
            wb = openpyxl.Workbook()
            headers = ['Panel', 'Run ID', 'Worksheet', 'Worksheet Date', 'Run Date', 'TAT']
            panels = ['BRCA', 'CRM', 'CRUK', 'NIPT', 'TAM', 'TSC', 'TSO', 'WCB']
            # Fill in raw data tab, panels tab and others tab
            tab_raw(wb, runs, headers)
            tab_panels(wb, runs, headers, panels)
            tab_other(wb, runs, headers, panels)
            # save and return workbook as response
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheet.sheet')
            output_name = 'attachment; filename="KPI_' + str(dates.start_date) + '_' + str(dates.end_date) + '.xlsx"'
            response['Content-Disposition'] = output_name
            wb.save(response)
            return response
    # if no data inputted, display form
    else:
        form = TatForm()
        template = loader.get_template('db/index.html')
        context = {'form': form,}
        return HttpResponse(template.render(context, request))
