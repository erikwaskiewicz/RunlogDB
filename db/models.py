from django.db import models
import json


class Instrument(models.Model):
    instrument_id = models.CharField(max_length=255, primary_key=True)
    instrument_type = models.CharField(max_length=255)

    def __str__(self):
        return self.instrument_id


class Run(models.Model):
    """
    Model for storing data about a particular NGS run, data comes from the RunInfo.xml,
    RunParameters.xml, Interops and SampleSheet.csv.
    Also stores raw JSON object of the input files.
    """
    run_id = models.CharField(max_length=255, primary_key=True)
    #worksheets = models.ManyToManyField('Worksheet')
    instrument = models.OneToOneField('Instrument', on_delete=models.CASCADE)

    instrument_date = models.DateField()
    setup_date = models.DateField(blank=True, null=True)
    samplesheet_date = models.DateField(blank=True, null=True)
    #TODO add worksheet date, or is this the same as samplesheet date?

    investigator = models.CharField(max_length=255, blank=True)
    experiment = models.CharField(max_length=255, blank=True)
    workflow = models.CharField(max_length=255, blank=True)
    application = models.CharField(max_length=255, blank=True)
    assay = models.CharField(max_length=255, blank=True)
    chemistry = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)

    num_reads = models.IntegerField()
    length_read1 = models.IntegerField()
    length_read2 = models.IntegerField(blank=True, null=True)
    num_indexes = models.IntegerField()
    length_index1 = models.IntegerField()
    length_index2 = models.IntegerField(blank=True, null=True)

    percent_q30 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    cluster_density = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    percent_pf = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    phasing = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    prephasing = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    error_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    percent_aligned = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    #TODO - make seperate table for sensitivity??
    #sensitivity = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    #sensitivity_lower_95ci = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    #sensitivity_upper_95ci = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    diagnostic_run = models.BooleanField()
    comments = models.TextField(blank=True)

    raw_runinfo_json = models.TextField()
    raw_runparameters_json = models.TextField()
    raw_samplesheet_json = models.TextField()

    def __str__(self):
        return self.run_id

    def runinfo_json(self):
        # turn textfield into json object
        return json.dumps(
            json.loads(self.raw_runinfo_json), 
            indent=2, separators=(',', ':')
        )

    def runparameters_json(self):
        # turn textfield into json object
        return json.dumps(
            json.loads(self.raw_runparameters_json), 
            indent=2, separators=(',', ':')
        )

    def samplesheet_json(self):
        # turn textfield into json object
        return json.dumps(
            json.loads(self.raw_samplesheet_json), 
            indent=2, separators=(',', ':')
        )


class Worksheet(models.Model):
    worksheet_id = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.worksheet_id


class WorksheetAnalysis(models.Model):
    unique_id = models.CharField(max_length=255, primary_key=True) # run+ws+analysis_count
    #samples = models.ManyToManyField('SampleRun')
    worksheet = models.OneToOneField('Worksheet', on_delete=models.CASCADE)
    run = models.ForeignKey('Run', on_delete=models.CASCADE)

    pipeline_name = models.CharField(max_length=255, blank=True)
    pipeline_version = models.CharField(max_length=255, blank=True)
    panel = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.unique_id

    def list_samples(self):
        """Make a string list of all samples in a worksheet"""
        #TODO check this function works for new database layout
        sample_analyses = SampleAnalysis.objects.filter(worksheet_analysis=self.unique_id)
        samples = [s.sample.sample_id for s in sample_analyses]
        return ', '.join(samples)

    def get_panel(self):
        """Turn panel code into the panel name recognised by the lab"""
        if self.panel == "NGHS-101X-WCB":
            return "WCB"
        elif self.panel == "NGHS-101X":
            return "CRM"
        elif self.panel == "NGHS-102X":
            return "BRCA"
        elif self.panel == "SMP2v2":
            return "CRUK"
        elif self.panel == "IlluminaTruSightCancer":
            return "TruSightCancer"
        elif self.panel == "IlluminaTruSightOne":
            return "TruSightOne"
        elif self.panel == "NGHS-201X":
            return "TAM"
        elif self.panel == "TruSightMyeloid":
            return "TruSightMyeloid"
        elif self.panel == "RochePanCancer":
            return "PanCancer"
        elif self.panel == "NIPT":
            return "NIPT"
        elif self.panel == "":
            return "Unknown"
        else:
            return self.panel


class Sample(models.Model):
    sample_id = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.sample_id


class SampleAnalysis(models.Model):
    unique_id = models.CharField(max_length=255, primary_key=True) #ws_analysis+sample_id
    sample = models.OneToOneField('Sample', on_delete=models.CASCADE)
    worksheet_analysis = models.ForeignKey('WorksheetAnalysis', on_delete=models.CASCADE)

    description = models.TextField(blank=True)
    sex = models.CharField(max_length=255, blank=True)

    i5_name = models.CharField(max_length=255, blank=True)
    i5_seq = models.CharField(max_length=255, blank=True)
    i7_name = models.CharField(max_length=255, blank=True)
    i7_seq = models.CharField(max_length=255, blank=True)
    sample_well = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.unique_id


class Fastqc(models.Model):
    """
    Model to store data from the FastQC output, there will be one entry per fastq file.
    There is a fastq file made for each lane and each read, so a run will usually have 2-4.
    """
    unique_id = models.CharField(max_length=255, primary_key=True) #samplerun + read + lane
    #link to sample analysis object
    sample = models.ForeignKey(
        'SampleAnalysis',
        on_delete=models.CASCADE,
    )
    read_group = models.CharField(max_length=255, blank=True)
    lane = models.CharField(max_length=255, blank=True)
    basic_statistics = models.CharField(max_length=255, blank=True)
    per_base_sequence_quality = models.CharField(max_length=255, blank=True)
    Per_tile_sequence_quality = models.CharField(max_length=255, blank=True)
    per_sequence_quality_scores = models.CharField(max_length=255, blank=True)
    per_base_sequence_content = models.CharField(max_length=255, blank=True)
    per_sequence_qc_content = models.CharField(max_length=255, blank=True)
    per_base_n_content = models.CharField(max_length=255, blank=True)
    sequence_length_distribution = models.CharField(max_length=255, blank=True)
    sequence_duplication_levels = models.CharField(max_length=255, blank=True)
    overrepresented_sequences = models.CharField(max_length=255, blank=True)
    adapter_content = models.CharField(max_length=255, blank=True)
    kmer_content = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.unique_id


class SampleMetrics(models.Model):
    """
    Model to store output from the Picard HS metrics program.
    One per sample.
    # TODO - is this run/ws level or sample level???
    """
    unique_id = models.ForeignKey(
        'Sample',
        on_delete=models.CASCADE,
    )
    run_id = models.ForeignKey(
        'Run',
        on_delete=models.CASCADE,
    )
    sample_id = models.CharField(max_length=255)
    bait_set = models.CharField(max_length=255)
    genome_size = models.BigIntegerField()
    bait_territory = models.BigIntegerField(blank=True, null=True) 
    target_territory = models.BigIntegerField(blank=True, null=True)
    bait_design_efficiency = models.BigIntegerField(blank=True, null=True)
    total_reads = models.IntegerField(blank=True, null=True)
    pf_reads = models.IntegerField(blank=True, null=True)
    pf_unique_reads = models.IntegerField(blank=True, null=True)
    pct_pf_reads = models.IntegerField(blank=True, null=True)
    pct_pf_uq_reads = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    pf_uq_reads_aligned = models.IntegerField(blank=True, null=True)
    pct_pf_uq_reads_aligned = models.IntegerField(blank=True, null=True) 
    pf_bases_aligned = models.IntegerField(blank=True, null=True)
    pf_uq_bases_aligned = models.IntegerField(blank=True, null=True)
    on_bait_bases = models.IntegerField(blank=True, null=True) 
    near_bait_bases = models.IntegerField(blank=True, null=True)
    off_bait_bases = models.IntegerField(blank=True, null=True)
    on_target_bases = models.IntegerField(blank=True, null=True)
    pct_selected_bases = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    pct_off_bait = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    on_bait_vs_selected = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    mean_bait_coverage = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    mean_target_coverage = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    median_target_coverage = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    max_target_coverage = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    pct_usable_bases_on_bait = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    pct_usable_bases_on_target = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    fold_enrichment = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    zero_cvg_targets_pct = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    pct_exc_dupe = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    pct_exc_mapq = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    pct_exc_baseq = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    pct_exc_overlap = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    pct_exc_off_target = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    fold_80_base_penalty = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    pct_target_bases_1x =  models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    pct_target_bases_2x = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    pct_target_bases_10x = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    pct_target_bases_20x = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    pct_target_bases_30x = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    pct_target_bases_40x = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    pct_target_bases_50x = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    pct_target_bases_100x = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    hs_library_size = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    hs_penalty_10x = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True) 
    hs_penalty_20x = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    hs_penalty_30x = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    hs_penalty_40x = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    hs_penalty_50x = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    hs_penalty_100x = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    at_dropout = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    gc_dropout = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    het_snp_sensitivity = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    het_snp_q = models.IntegerField(blank=True, null=True) 

    def __str__(self):
        return self.sample_id
