from django.db import models
import json

class Sample(models.Model):
    sample_id = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.sample_id


class Instrument(models.Model):
    instrument_id = models.CharField(max_length=100, primary_key=True)
    instrument_type = models.CharField(max_length=100)

    def __str__(self):
        return self.instrument_id


class Run(models.Model):
    """
    Table for storing information common to all NGS runs, regardless of instrument type
    """
    run_id = models.CharField(max_length=100, primary_key=True)
    worksheets = models.ManyToManyField('Worksheet')
    instrument = models.ForeignKey('Instrument', on_delete=models.CASCADE)

    instrument_date = models.DateField()
    setup_date = models.DateField(blank=True, null=True)
    samplesheet_date = models.CharField(max_length=100, blank=True, null=True)

    investigator = models.CharField(max_length=100, null=True)
    experiment = models.CharField(max_length=100, null=True)
    workflow = models.CharField(max_length=100, null=True)
    application = models.CharField(max_length=100, null=True)
    assay = models.CharField(max_length=100, null=True)
    chemistry = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=200, null=True)

    num_reads = models.IntegerField()
    length_read1 = models.IntegerField()
    length_read2 = models.IntegerField(null=True)
    num_indexes = models.IntegerField()
    length_index1 = models.IntegerField()
    length_index2 = models.IntegerField(null=True)

    percent_q30 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    cluster_density = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    percent_pf = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    phasing = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    prephasing = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    error_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    percent_aligned = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    #sensitivity = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    #sensitivity_lower_95ci = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    #sensitivity_upper_95ci = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    diagnostic_run = models.BooleanField()
    comments = models.TextField(blank=True, null=True)

    raw_runinfo_json = models.TextField()
    raw_runparameters_json = models.TextField()
    raw_samplesheet_json = models.TextField()

    def __str__(self):
        return self.run_id

    def runinfo_json(self):
        # turn textfield into json object
        return json.loads(self.raw_runinfo_json)


class Worksheet(models.Model):
    ws_id = models.CharField(max_length=200, primary_key=True)     #"Sample_Plate":"18-9110",
    samples = models.ManyToManyField('SampleRun')

    pipeline_name = models.CharField(max_length=200, null=True)
    pipeline_version = models.CharField(max_length=200, null=True)
    panel = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.ws_id


class SampleRun(models.Model):
    unique_id = models.CharField(max_length=100, primary_key=True) #run+ws+sample ids
    sample_obj = models.ForeignKey('Sample', on_delete=models.CASCADE)

    description = models.TextField(null=True)                      #pipelineName=SomaticAmplicon;pipelineVersion=1.7.5;panel=NGHS-201X
    sex = models.CharField(max_length=10, null=True)

    i5_name = models.CharField(max_length=50, null=True)                              #"I5_Index_ID":"Bc1",
    i5_seq = models.CharField(max_length=50, null=True)                               #"index2":"ATCACG"
    i7_name = models.CharField(max_length=50, null=True)                              #"I7_Index_ID":"Bc1",
    i7_seq = models.CharField(max_length=50, null=True)                              #"index":"ATCACG"
    sample_well = models.CharField(max_length=50, null=True)
    sample_project = models.CharField(max_length=50, null=True)    #"Sample_Project":"",  usually empty-remove????

    def __str__(self):
        return self.unique_id








'''
class SampleMetrics(models.Model):
    UniqueID = models.ForeignKey(
        'Sample',
        on_delete=models.CASCADE,
    )
    UKW = 'Not Specified'
    run_id = models.ForeignKey(
        'Runlog',
        on_delete=models.CASCADE,
    )
    SampleID = models.CharField(max_length=10)
    BAIT_SET = models.CharField(max_length=100)
    GENOME_SIZE = models.BigIntegerField()
    BAIT_TERRITORY = models.BigIntegerField(blank=True, null=True) 
    TARGET_TERRITORY = models.BigIntegerField(blank=True, null=True)
    BAIT_DESIGN_EFFICIENCY = models.BigIntegerField(blank=True, null=True)
    TOTAL_READS = models.IntegerField(blank=True, null=True)
    PF_READS = models.IntegerField(blank=True, null=True)
    PF_UNIQUE_READS = models.IntegerField(blank=True, null=True)
    PCT_PF_READS = models.IntegerField(blank=True, null=True)
    PCT_PF_UQ_READS = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PF_UQ_READS_ALIGNED = models.IntegerField(blank=True, null=True)
    PCT_PF_UQ_READS_ALIGNED = models.IntegerField(blank=True, null=True) 
    PF_BASES_ALIGNED = models.IntegerField(blank=True, null=True)
    PF_UQ_BASES_ALIGNED = models.IntegerField(blank=True, null=True)
    ON_BAIT_BASES = models.IntegerField(blank=True, null=True) 
    NEAR_BAIT_BASES = models.IntegerField(blank=True, null=True)
    OFF_BAIT_BASES = models.IntegerField(blank=True, null=True)
    ON_TARGET_BASES = models.IntegerField(blank=True, null=True)
    PCT_SELECTED_BASES = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_OFF_BAIT = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    ON_BAIT_VS_SELECTED = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    MEAN_BAIT_COVERAGE = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    MEAN_TARGET_COVERAGE = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    MEDIAN_TARGET_COVERAGE = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    MAX_TARGET_COVERAGE = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_USABLE_BASES_ON_BAIT = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_USABLE_BASES_ON_TARGET = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    FOLD_ENRICHMENT = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    ZERO_CVG_TARGETS_PCT = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_EXC_DUPE = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_EXC_MAPQ = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_EXC_BASEQ = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_EXC_OVERLAP = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_EXC_OFF_TARGET = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    FOLD_80_BASE_PENALTY = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_TARGET_BASES_1X =  models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_TARGET_BASES_2X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_TARGET_BASES_10X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_TARGET_BASES_20X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_TARGET_BASES_30X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_TARGET_BASES_40X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_TARGET_BASES_50X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    PCT_TARGET_BASES_100X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    HS_LIBRARY_SIZE = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    HS_PENALTY_10X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True) 
    HS_PENALTY_20X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    HS_PENALTY_30X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    HS_PENALTY_40X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    HS_PENALTY_50X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    HS_PENALTY_100X = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    AT_DROPOUT = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    GC_DROPOUT = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    HET_SNP_SENSITIVITY = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    HET_SNP_Q = models.IntegerField(blank=True, null=True) 
    
class FastQC(models.Model):
    UniqueID = models.ForeignKey(
        'Sample',
        on_delete=models.CASCADE,
    )
    Read_Group = models.CharField(max_length=50, blank=True, null=True)
    Lane = models.CharField(max_length=50, blank=True, null=True)
    PASS = 'PASS'
    WARN ='WARN'
    FAIL = 'FAIL'
    UKW = 'UNKNOWN'
    fastqcheck_CHOICES = (
        (PASS, 'PASS'),
        (WARN, 'WARN'),
        (FAIL, 'FAIL'),
    )
    Basic_Statistics = models.CharField(max_length=4, choices=fastqcheck_CHOICES, blank=True, default=UKW )
    Per_base_sequence_quality = models.CharField(max_length=4, choices=fastqcheck_CHOICES, blank=True, default=UKW )
    Per_tile_sequence_quality = models.CharField(max_length=4, choices=fastqcheck_CHOICES, blank=True, default=UKW )
    Per_sequence_quality_scores = models.CharField(max_length=4, choices=fastqcheck_CHOICES, blank=True, default=UKW )
    Per_base_sequence_content = models.CharField(max_length=4, choices=fastqcheck_CHOICES, blank=True, default=UKW )
    Per_sequence_GC_content = models.CharField(max_length=4, choices=fastqcheck_CHOICES, blank=True, default=UKW )
    Per_base_N_content = models.CharField(max_length=4, choices=fastqcheck_CHOICES, blank=True, default=UKW )
    Sequence_Length_Distribution = models.CharField(max_length=4, choices=fastqcheck_CHOICES, blank=True, default=UKW )
    Sequence_Duplication_Levels = models.CharField(max_length=4, choices=fastqcheck_CHOICES, blank=True, default=UKW )
    Overrepresented_sequences = models.CharField(max_length=4, choices=fastqcheck_CHOICES, blank=True, default=UKW )
    Adapter_Content = models.CharField(max_length=4, choices=fastqcheck_CHOICES, blank=True, default=UKW )
    Kmer_Content = models.CharField(max_length=4, choices=fastqcheck_CHOICES, blank=True, default=UKW )
 
'''