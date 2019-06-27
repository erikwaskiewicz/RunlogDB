from django.contrib import admin
from .models import Run, Nextseq, Hiseq, Miseq, Worksheet, Sample       #, SampleMetrics, FastQC


# Register your models here.
class RunAdmin(admin.ModelAdmin):
    list_display = ('run_id', 'experiment', 'instrument_date', 'samplesheet_date')   #'pipeline', 
admin.site.register(Run, RunAdmin)

admin.site.register(Worksheet)

admin.site.register(Sample)

admin.site.register(Nextseq)

admin.site.register(Hiseq)

admin.site.register(Miseq)

#admin.site.register(SampleMetrics)

#admin.site.register(FastQC)

