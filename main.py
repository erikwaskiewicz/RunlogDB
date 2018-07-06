"""
----------------------------------------------------------------------------------------------------
main.py
-- parse data from runInfo.xml and add to runinfo dictionary
-- parse data from samplesheet.csv and add to samplesheet dictionary
-- parse data from interops files and add to interop dictionary
-- add data from dictionaries above to runlog table in RunlogDB
-- determine if run was from hiseq or miseq
-- add data from RunParameters.xml file to either hiseq or miseq table in RunlogDB
----------------------------------------------------------------------------------------------------
"""

# Import scripts
from scripts import add_to_db, parse_interop, parse_runinfo, parse_runparameters, parse_samplesheet
import sys

# Load run folder
run_folder = sys.argv[1]
#run_folder = r"/Users/erik/Documents/RunLog"

# ----------------------------------------------------------------------------------------------------
# PARSE RUNINFO

# Create empty runinfo dictionary and define parameters to extract from RunInfo
runinfo_dict = {}
runinfo_values = [["Id", "get"], 
                  ["Instrument", "find"], 
                  ["Date", "find"]]

# data from runinfo_values array
for item in runinfo_values:
    parse_runinfo.parse1(run_folder, runinfo_dict, item[0], item[1])

# number of cycles
parse_runinfo.parse2(run_folder, runinfo_dict)


# ----------------------------------------------------------------------------------------------------
# PARSE SAMPLESHEET

# create empty dictionary and define parameters to extract
samplesheet_dict = {}
samplesheet_values1 = ["Investigator Name", "Experiment Name", "Date", "Workflow", "Application", 
    "Assay", "Description", "Chemistry"]
samplesheet_values2 = [["Plates", "Sample_Plate"], 
                       ["Description2", "Description"], 
                       ["Samples", "Sample_ID"], 
                       ["I7", "I7_Index_ID"], 
                       ["I5", "I5_Index_ID"]]

# data from samplesheet values array
for item in samplesheet_values1:
    parse_samplesheet.parse1(run_folder, samplesheet_dict, item)

# plates, description, samples and indexes
for item in samplesheet_values2:
    parse_samplesheet.parse2(run_folder, samplesheet_dict, item[0], item[1])

# pipeline
parse_samplesheet.parse3(samplesheet_dict)

# ----------------------------------------------------------------------------------------------------
# PARSE INTEROPS

# create empty dictionary
interop_dict = {}

# parse (parameters set in function)
parse_interop.parse(run_folder, interop_dict)


# ----------------------------------------------------------------------------------------------------
# ADD TO DATABASE

add_to_db.runinfo_add(runinfo_dict, samplesheet_dict, interop_dict)


# ----------------------------------------------------------------------------------------------------
# PARSE RUNPARAMETERS

# hiseq
if parse_runparameters.instrument_type(run_folder) == "HiSeq":
    # create empty dictionary and define variables to be extracted
    hiseq_dict = {}
    runparameter_values1 = ["RunID", "WorkFlowType", "PairEndFC", "Flowcell", "Sbs", "Pe", "Index", 
        "ClusteringChoice", "RapidRunChemistry", "RunMode", "ApplicationName", "ApplicationVersion", 
        "FPGAVersion", "CPLDVersion", "RTAVersion", "ChemistryVersion", "CameraFirmware", "CameraDriver"]
    runparameter_values2 = [["Sbs", "SbsReagentKit"], 
                            ["Index", "ReagentKit"]]

    # extract variables
    for item in runparameter_values1:
        parse_runparameters.hiseq1(run_folder, hiseq_dict, item)
    for item in runparameter_values2:
        parse_runparameters.hiseq2(run_folder, hiseq_dict, item[0], item[1])

    # upload data to database
    add_to_db.hiseq_add(hiseq_dict)


# ----------------------------------------------------------------------------------------------------
# miseq
if parse_runparameters.instrument_type(run_folder) == "MiSeq":
    # create empty dictionary and define variables to be extracted
    miseq_dict = {}
    runparameter_values1 = ["RunID", "MCSVersion", "RTAVersion"]
    runparameter_values2 = [["FlowcellRFIDTag", "SerialNumber"],
                            ["FlowcellRFIDTag", "PartNumber"],
                            ["FlowcellRFIDTag", "ExpirationDate"],
                            ["PR2BottleRFIDTag", "SerialNumber"],
                            ["PR2BottleRFIDTag", "PartNumber"],
                            ["PR2BottleRFIDTag", "ExpirationDate"],
                            ["ReagentKitRFIDTag", "SerialNumber"],
                            ["ReagentKitRFIDTag", "PartNumber"],
                            ["ReagentKitRFIDTag", "ExpirationDate"]]

    # extract variables
    for item in runparameter_values1:
        parse_runparameters.miseq1(run_folder, miseq_dict, item)

    for item in runparameter_values2:
        parse_runparameters.miseq2(run_folder, miseq_dict, item[0], item[1])

    # upload data to database
    add_to_db.miseq_add(miseq_dict)

# ----------------------------------------------------------------------------------------------------
# nextseq
if parse_runparameters.instrument_type(run_folder) == "NextSeq":
    # create empty dictionary and define variables to be extracted
    nextseq_dict = {}
    runparameter_values1 = ["RunID", "InstrumentID", "RTAVersion", "SystemSuiteVersion", "FlowCellSerial",
        "PR2BottleSerial", "ReagentKitSerial", "ExperimentName", "LibraryID", "Chemistry", "FocusMethod", 
        "SurfaceToScan", "IsPairedEnd", "CustomReadOnePrimer", "CustomReadTwoPrimer", "CustomIndexPrimer", 
        "CustomIndexTwoPrimer", "UsesCustomReadOnePrimer", "UsesCustomReadTwoPrimer", 
        "UsesCustomIndexPrimer", "UsesCustomIndexTwoPrimer", "RunManagementType", "BaseSpaceRunId", 
        "BaseSpaceRunMode", "ComputerName", "MaxCyclesSupportedByReagentKit"]
    runparameter_values2 = [["Setup", "ApplicationVersion"],
                            ["Setup", "ApplicationName"]]

    # extract variables
    for item in runparameter_values1:
        parse_runparameters.nextseq1(run_folder, nextseq_dict, item)

    for item in runparameter_values2:
        parse_runparameters.nextseq2(run_folder, nextseq_dict, item[0], item[1])

    # upload data to database
    add_to_db.nextseq_add(nextseq_dict)
