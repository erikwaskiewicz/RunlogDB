import sqlite3


DB = '/Users/erik/Projects/RunlogDB/runlog/runlogdb.sqlite3'

def runinfo_add(runinfo_dict, samplesheet_dict, interop_dict):
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    cursor.execute(''' INSERT INTO db_runlog (
            run_id, 
            instrument, 
            instrument_date, 
            num_cycles1,
            num_cycles2, 
            investigator, 
            experiment, 
            samplesheet_date, 
            workflow, 
            application, 
            assay, 
            description, 
            chemistry,
            plates,
            description2,
            samples,
            I7,
            I5,
            pipeline,
            percent_Q30,
            cluster_density,
            percent_pf,
            phasing,
            prephasing,
            error_rate,
            percent_aligned
            )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''',
           (runinfo_dict["Id"],
            runinfo_dict["Instrument"],
            runinfo_dict["Date"],
            runinfo_dict["num_cycles1"],
            runinfo_dict["num_cycles2"],
            samplesheet_dict["Investigator Name"],
            samplesheet_dict["Experiment Name"],
            samplesheet_dict["Date"],
            samplesheet_dict["Workflow"],
            samplesheet_dict["Application"],
            samplesheet_dict["Assay"],
            samplesheet_dict["Description"],
            samplesheet_dict["Chemistry"],
            samplesheet_dict["Plates"],
            samplesheet_dict["Description2"],
            samplesheet_dict["Samples"],
            samplesheet_dict["I7"],
            samplesheet_dict["I5"],
            samplesheet_dict["Pipeline"],
            interop_dict["Percent Q30"],
            interop_dict["Cluster density"],
            interop_dict["Percent PF"],
            interop_dict["Phasing"],
            interop_dict["Prephasing"],
            interop_dict["Error rate"],
            interop_dict["Aligned"]))
    db.commit()
    db.close()


def miseq_add(dictionary):
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    cursor.execute(''' INSERT INTO db_miseq (
            run_id_id, 
            MCS_version, 
            RTA_version, 
            flowcell_serial_no, 
            flowcell_part_no, 
            flowcell_expiry, 
            PR2_serial_no, 
            PR2_part_no, 
            PR2_expiry,
            reagent_serial_no, 
            reagent_part_no, 
            reagent_expiry
            )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''',
           (dictionary["RunID"],
            dictionary["MCSVersion"],
            dictionary["RTAVersion"],
            dictionary["FlowcellRFIDTagSerialNumber"],
            dictionary["FlowcellRFIDTagPartNumber"],
            dictionary["FlowcellRFIDTagExpirationDate"],
            dictionary["PR2BottleRFIDTagSerialNumber"],
            dictionary["PR2BottleRFIDTagPartNumber"],
            dictionary["PR2BottleRFIDTagExpirationDate"],
            dictionary["ReagentKitRFIDTagSerialNumber"],
            dictionary["ReagentKitRFIDTagPartNumber"],
            dictionary["ReagentKitRFIDTagExpirationDate"]))
    db.commit()
    db.close()


def hiseq_add(dictionary):
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    cursor.execute(''' INSERT INTO db_hiseq (
            run_id_id, 
            workflow_type,
            paired_end,
            flowcell_version,
            sbs_version,
            pe_version,
            index_version,
            clustering_choice,
            rapid_run_chemistry,
            run_mode,
            application_name,
            application_version,
            FPGA_version,
            CPLD_version,
            RTA_version,
            chemistry_version,
            camera_firmware,
            camera_driver,
            sbs_reagent_kit,
            index_reagent_kit
            )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''',
           (dictionary["RunID"],
            dictionary["WorkFlowType"],
            dictionary["PairEndFC"],
            dictionary["Flowcell"],
            dictionary["Sbs"],
            dictionary["Pe"],
            dictionary["Index"],
            dictionary["ClusteringChoice"],
            dictionary["RapidRunChemistry"],
            dictionary["RunMode"],
            dictionary["ApplicationName"],
            dictionary["ApplicationVersion"],
            dictionary["FPGAVersion"],
            dictionary["CPLDVersion"],
            dictionary["RTAVersion"],
            dictionary["ChemistryVersion"],
            dictionary["CameraFirmware"],
            dictionary["CameraDriver"],
            dictionary["SbsSbsReagentKit"],
            dictionary["IndexReagentKit"]))
    db.commit()
    db.close()


def nextseq_add(dictionary):
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    cursor.execute(''' INSERT INTO db_nextseq (
            run_id_id,
            instrument_id,
            RTA_version,
            systemsuite_version,
            flowcell_serial,
            PR2_serial_no,
            reagent_serial_no,
            experiment_name,
            library_id,
            chemistry,
            focus_method,
            surface_to_scan,
            paired_end,
            custom_R1_primer,
            custom_R2_perimer,
            custom_index_primer,
            custom_index2_primer,
            uses_custom_R1_primer,
            uses_custom_R2_perimer,
            uses_custom_index_primer,
            uses_custom_index2_primer,
            run_management_type,
            basespace_id,
            basespace_runmode,
            computer_name,
            max_reagent_kit_cycles,
            application_name,
            application_version
            )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''',
           (dictionary["RunID"],
            dictionary["InstrumentID"],
            dictionary["RTAVersion"],
            dictionary["SystemSuiteVersion"],
            dictionary["FlowCellSerial"],
            dictionary["PR2BottleSerial"],
            dictionary["ReagentKitSerial"],
            dictionary["ExperimentName"],
            dictionary["LibraryID"],
            dictionary["Chemistry"],
            dictionary["FocusMethod"],
            dictionary["SurfaceToScan"],
            dictionary["IsPairedEnd"],
            dictionary["CustomReadOnePrimer"],
            dictionary["CustomReadTwoPrimer"],
            dictionary["CustomIndexPrimer"],
            dictionary["CustomIndexTwoPrimer"],
            dictionary["UsesCustomReadOnePrimer"],
            dictionary["UsesCustomReadTwoPrimer"], 
            dictionary["UsesCustomIndexPrimer"],
            dictionary["UsesCustomIndexTwoPrimer"], 
            dictionary["RunManagementType"],
            dictionary["BaseSpaceRunId"],
            dictionary["BaseSpaceRunMode"], 
            dictionary["ComputerName"],
            dictionary["MaxCyclesSupportedByReagentKit"],
            dictionary["ApplicationName"],
            dictionary["ApplicationVersion"]))
    db.commit()
    db.close()
