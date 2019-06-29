import xml.etree.ElementTree as ET
import os.path
import xmltodict
import json


def get_runparameters_dict(run_folder):
    # get path to runparametrs file - first R could be either upper or lower case
    runparameter_options = [run_folder + r"/RunParameters.xml", run_folder + r"/runParameters.xml"] # TODO use path package
    if os.path.isfile(runparameter_options[0]):
        runparameters_path = runparameter_options[0]
    elif os.path.isfile(runparameter_options[1]):
        runparameters_path = runparameter_options[1]
    else:
        exit(f"ERROR  Could not open file {runparameter_options[0]} or {runparameter_options[1]}") # TODO add logging

    # turn XML file into a dictionary
    with open(runparameters_path) as f:
        runinfo_dict = xmltodict.parse(f.read())

    return runinfo_dict


def get_instrument_type(instrument_id):
    if instrument_id.startswith('M'):
        instrument_type = 'MiSeq'
    elif instrument_id.startswith('D'):
        instrument_type = 'HiSeq'
    elif instrument_id.startswith('NB'):
        instrument_type = 'NextSeq'
    else:
        instrument_type = ''

    return instrument_type
