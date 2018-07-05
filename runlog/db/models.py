from django.db import models

class Runlog(models.Model):
    run_id = models.CharField(max_length=100, primary_key=True)
    diagnostic_run = models.BooleanField()
    instrument = models.CharField(max_length=100)
    instrument_date = models.DateField()
    setup_date = models.DateField(blank=True, null=True)
    samplesheet_date = models.CharField(max_length=100, blank=True, null=True)
    investigator = models.CharField(max_length=100, null=True)
    experiment = models.CharField(max_length=100, null=True)
    plates = models.CharField(max_length=200, null=True)
    pipeline = models.CharField(max_length=200, null=True)
    num_cycles1 = models.IntegerField()
    num_cycles2 = models.IntegerField()
    workflow = models.CharField(max_length=100, null=True)
    application = models.CharField(max_length=100, null=True)
    assay = models.CharField(max_length=100, null=True)
    chemistry = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=200, null=True)
    description2 = models.TextField(null=True)
    samples = models.TextField(null=True)
    I7 = models.TextField(null=True)
    I5 = models.TextField(null=True)
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


class Input(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    