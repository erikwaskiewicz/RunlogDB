from django.contrib import admin
from .models import Sample, Instrument, Run, Worksheet, SampleRun, Fastqc, SampleMetrics 


# Register your models here.
class RunAdmin(admin.ModelAdmin):
    list_display = ('run_id', 'experiment', 'instrument_date', 'samplesheet_date',)   #'pipeline', 
admin.site.register(Run, RunAdmin)

class WorksheetAdmin(admin.ModelAdmin):
    list_display = ('ws_id', 'panel', 'pipeline_name', 'pipeline_version',)
admin.site.register(Worksheet, WorksheetAdmin)

admin.site.register(Sample)

class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('instrument_id', 'instrument_type',)
admin.site.register(Instrument, InstrumentAdmin)

class SampleRunAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'sample_obj',)
admin.site.register(SampleRun, SampleRunAdmin)

class FastqcAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'sample', 'read_group', 'lane',)
admin.site.register(Fastqc, FastqcAdmin)

class SampleMetricsAdmin(admin.ModelAdmin):
    list_display = ('unique_id',)
admin.site.register(SampleMetrics, SampleMetricsAdmin)
