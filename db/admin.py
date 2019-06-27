from django.contrib import admin
from .models import Runlog, Nextseq, Hiseq, Miseq       #, SampleMetrics, FastQC


# Register your models here.
class RunlogAdmin(admin.ModelAdmin):
    list_display = ('run_id', 'experiment', 'instrument_date', 'samplesheet_date')   #'pipeline', 
admin.site.register(Runlog, RunlogAdmin)

admin.site.register(Nextseq)

admin.site.register(Hiseq)

admin.site.register(Miseq)

#admin.site.register(SampleMetrics)

#admin.site.register(FastQC)

