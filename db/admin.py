from django.contrib import admin
from .models import Sample, Instrument, Run, Worksheet, SampleRun       #, SampleMetrics, FastQC, Nextseq, Hiseq, Miseq, 


# Register your models here.
class RunAdmin(admin.ModelAdmin):
    list_display = ('run_id', 'experiment', 'instrument_date', 'samplesheet_date')   #'pipeline', 
admin.site.register(Run, RunAdmin)
admin.site.register(Worksheet)
admin.site.register(Sample)
admin.site.register(Instrument)
admin.site.register(SampleRun)



#admin.site.register(SampleMetrics)
#admin.site.register(FastQC)

