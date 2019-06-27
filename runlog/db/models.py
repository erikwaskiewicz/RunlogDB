from django.db import models

# Table for storing information common to all NGS runs, regardless of instrument type
class Runlog(models.Model):
    run_id = models.CharField(max_length=100, primary_key=True)
    diagnostic_run = models.BooleanField()
    instrument = models.CharField(max_length=100)
    instrument_date = models.DateField()
    setup_date = models.DateField(blank=True, null=True)
    samplesheet_date = models.CharField(max_length=100, blank=True, null=True)
    investigator = models.CharField(max_length=100, null=True)
    experiment = models.CharField(max_length=100, null=True)
    read1 = models.IntegerField()
    read2 = models.IntegerField()
    #plates = models.CharField(max_length=200, null=True)
    pipeline = models.CharField(max_length=200, null=True)
    num_cycles1 = models.IntegerField()
    num_cycles2 = models.IntegerField()
    workflow = models.CharField(max_length=100, null=True)
    application = models.CharField(max_length=100, null=True)
    assay = models.CharField(max_length=100, null=True)
    chemistry = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=200, null=True)
    #description2 = models.TextField(null=True)
    #samples = models.TextField(null=True)
    #I7 = models.TextField(null=True)
    #I5 = models.TextField(null=True)
    percent_Q30 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    cluster_density = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    percent_pf = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    phasing = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    prephasing = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    error_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    percent_aligned = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    sensitivity = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    sensitivity_lower_95ci = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    sensitivity_upper_95ci = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.run_id



class Worksheet(models.Model):
    ws_id = models.CharField(max_length=200, primary_key=True) #"Sample_Plate":"18-9110",
    run_id = models.ForeignKey(
        'Runlog',
        on_delete=models.CASCADE,
    )
    pipelineName = models.CharField(max_length=200, null=True)
    pipelineVersion = models.CharField(max_length=200, null=True)
    panel = models.CharField(max_length=200, null=True)
    
    def pipeline (self):
        samples = SampleRun.objects.filter(ws_id= self) #forgot what the code is doing here - ask erik 
        panels_list = []
        for sample in samples:
            panel = sample.pipeline()   #pipeline function called from the Sample table is defined in the WS sample(s) variable
            panels_list.append(panel)
        panel_unique = []
        for panel in panel_list:
            if panel not in panel_unique:
                panel_unique.append(panel)
            if panel == "":
                panel_unique.remove(panel)

        panels = ",".join(panels)

        return panels 
           


class SampleRun(models.Model):
    UniqueID = models.CharField(max_length=100, primary_key=True)
    ws_id =models.ForeignKey(
        'Worksheet',
        on_delete=models.CASCADE,
    )
    run_id = models.ForeignKey(
        'Runlog',
        on_delete=models.CASCADE,
    )
    sample_id = models.TextField(null=True)
    I7 = models.TextField(null=True) #"I7_Index_ID":"Bc1",
    I5 = models.TextField(null=True) #"index":"ATCACG"
    description = models.TextField(null=True) #pipelineName=SomaticAmplicon;pipelineVersion=1.7.5;panel=NGHS-201X
    sample_well = IntegerFeild()
    sample_project = models.Charfeild(max_length=50, null=True)  #"Sample_Project":"",
    sex = models.Charfeild(max_length=10, null=True)



    def pipeline(self):

        panel_list = self.description.split(',')
        for panel in panel_list:
            if "NGHS-101X-WCB" in var:
                return "WCB"
            elif "NGHS-101X" in var:
                return "CRM"
            elif "NGHS-102X" in var:
                return "BRCA"
            elif "CRUK" in var:
                return "CRUK"
            elif "TruSightCancer" in var:
                return "TruSightCancer"
            elif "TruSightOne" in var:
                return "TruSightOne"
            elif "NGHS-201X" in var:
                return "TAM"
            # Currently don't have a better identifier for NIPT
            elif "cfDNA" in Runlog.description:
                return "NIPT"



# Table for storing MiSeq specific run parameters
class Miseq(models.Model):
    run_id = models.ForeignKey(
        'Runlog',
        on_delete=models.CASCADE,
    )
    MCS_version = models.CharField(max_length=100)
    RTA_version = models.CharField(max_length=100)
    flowcell_serial_no = models.CharField(max_length=100)
    flowcell_part_no = models.CharField(max_length=100)
    flowcell_expiry = models.CharField(max_length=100)
    PR2_serial_no = models.CharField(max_length=100)
    PR2_part_no = models.CharField(max_length=100)
    PR2_expiry = models.CharField(max_length=100)
    reagent_serial_no = models.CharField(max_length=100)
    reagent_part_no = models.CharField(max_length=100)
    reagent_expiry = models.CharField(max_length=100)
    def __str__(self):
        return self.run_id_id


# Table for storing HiSeq specific run parameters
class Hiseq(models.Model):
    run_id = models.ForeignKey(
        'Runlog',
        on_delete=models.CASCADE,
    )
    workflow_type = models.CharField(max_length=100)
    paired_end = models.CharField(max_length=100)
    flowcell_version = models.CharField(max_length=100)
    sbs_version = models.CharField(max_length=100)
    pe_version = models.CharField(max_length=100, null=True)
    index_version = models.CharField(max_length=100)
    clustering_choice = models.CharField(max_length=100)
    rapid_run_chemistry = models.CharField(max_length=100)
    run_mode = models.CharField(max_length=100)
    application_name = models.CharField(max_length=100)
    application_version = models.CharField(max_length=100)
    FPGA_version = models.CharField(max_length=100)
    CPLD_version = models.CharField(max_length=100)
    RTA_version = models.CharField(max_length=100)
    chemistry_version = models.CharField(max_length=100)
    camera_firmware = models.CharField(max_length=100)
    camera_driver = models.CharField(max_length=100)
    sbs_reagent_kit = models.CharField(max_length=100)
    index_reagent_kit = models.CharField(max_length=100)
    def __str__(self):
        return self.run_id_id


# Table for storing NextSeq specific run parameters
class Nextseq(models.Model):
    run_id = models.ForeignKey(
        'Runlog',
        on_delete=models.CASCADE,
    )
    instrument_id = models.CharField(max_length=100)
    application_name = models.CharField(max_length=100)
    application_version = models.CharField(max_length=100)
    RTA_version = models.CharField(max_length=100)
    systemsuite_version = models.CharField(max_length=100)
    flowcell_serial = models.CharField(max_length=100)
    PR2_serial_no = models.CharField(max_length=100)
    reagent_serial_no = models.CharField(max_length=100)
    experiment_name = models.CharField(max_length=100)
    library_id = models.CharField(max_length=100)
    chemistry = models.CharField(max_length=100)
    focus_method = models.CharField(max_length=100)
    surface_to_scan = models.CharField(max_length=100)
    paired_end = models.CharField(max_length=100)
    custom_R1_primer = models.CharField(max_length=100)
    custom_R2_perimer = models.CharField(max_length=100)
    custom_index_primer = models.CharField(max_length=100)
    custom_index2_primer = models.CharField(max_length=100)
    uses_custom_R1_primer = models.CharField(max_length=100)
    uses_custom_R2_perimer = models.CharField(max_length=100)
    uses_custom_index_primer = models.CharField(max_length=100)
    uses_custom_index2_primer = models.CharField(max_length=100)
    run_management_type = models.CharField(max_length=100)
    basespace_id = models.CharField(max_length=100)
    basespace_runmode = models.CharField(max_length=100)
    computer_name = models.CharField(max_length=100)
    max_reagent_kit_cycles = models.CharField(max_length=100)
    def __str__(self):
        return self.run_id_id


# Table for storing input values from the frontend. No data is saved to this table.
class Input(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    run_id = models.CharField(max_length=100, blank=True, null=True)
    experiment = models.CharField(max_length=100, blank=True, null=True)
    samples = models.CharField(max_length=100, blank=True, null=True)
    pipeline = models.CharField(max_length=100, blank=True, null=True)



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
 
























