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









'''
def instrument_type(run_folder):
    get_variables(run_folder)
    if runparameters.find("Setup").find("ApplicationName").text == "HiSeq Control Software":
        instrument = "HiSeq"
    elif runparameters.find("Setup").find("ApplicationName").text == "MiSeq Control Software":
        instrument = "MiSeq"
    elif runparameters.find("Setup").find("ApplicationName").text == "NextSeq Control Software":
        instrument = "NextSeq"
    else:
        exit("ERROR  Instrument type could not be determined")
    return instrument


def miseq1(run_folder, dictionary, runparameter_value):
    get_variables(run_folder)
    for parameter in runparameters.iter("RunParameters"):
        if parameter.find(runparameter_value) is not None:
            dictionary[runparameter_value] = parameter.find(runparameter_value).text
        else:
            dictionary[runparameter_value] = "Null"


def miseq2(run_folder, dictionary, runparameter_value1, runparameter_value2):
    get_variables(run_folder)
    for parameter in runparameters.iter("RunParameters"):
        if parameter.find(runparameter_value1).find(runparameter_value2) is not None:
            dictionary[runparameter_value1 + runparameter_value2] = parameter.find(runparameter_value1).find(runparameter_value2).text
        else:
            dictionary[runparameter_value1 + runparameter_value2] = "Null"


def hiseq1(run_folder, dictionary, runparameter_value):
    get_variables(run_folder)
    for parameter in runparameters.iter("RunParameters"):
        if parameter.find("Setup").find(runparameter_value) is not None:
            dictionary[runparameter_value] = parameter.find("Setup").find(runparameter_value).text
        else:
            dictionary[runparameter_value] = "Null"


def hiseq2(run_folder, dictionary, runparameter_value1, runparameter_value2):
    get_variables(run_folder)
    for parameter in runparameters.iter("RunParameters"):
        if parameter.find("Setup").find("ReagentKits").find(runparameter_value1).find(runparameter_value2).find("ID") is not None:
            dictionary[runparameter_value1 + runparameter_value2] = parameter.find("Setup").find("ReagentKits").find(runparameter_value1).find(runparameter_value2).find("ID").text
        else:
            dictionary[runparameter_value1 + runparameter_value2] ="Null"


def nextseq1(run_folder, dictionary, runparameter_value):
    get_variables(run_folder)
    for parameter in runparameters.iter("RunParameters"):
        if parameter.find(runparameter_value) is not None:
            dictionary[runparameter_value] = parameter.find(runparameter_value).text
        else:
            dictionary[runparameter_value] = "Null"


def nextseq2(run_folder, dictionary, runparameter_value1, runparameter_value2):
    get_variables(run_folder)
    for parameter in runparameters.iter("RunParameters"):
        if parameter.find(runparameter_value1).find(runparameter_value2) is not None:
            dictionary[runparameter_value2] = parameter.find(runparameter_value1).find(runparameter_value2).text
        else:
            dictionary[runparameter_value2] ="Null"
'''