import xml.etree.ElementTree as ET
import os.path


def get_variables(run_folder):
    runparameter_options = [run_folder + r"/RunParameters.xml", run_folder + r"/runParameters.xml"]
    if os.path.isfile(runparameter_options[0]) is True:
        runparameters_path = runparameter_options[0]
    elif os.path.isfile(runparameter_options[1]) is True:
        runparameters_path = runparameter_options[1]
    else:
        exit("ERROR  Could not open file " + runparameter_options[0] + " or " + runparameter_options[1])

    runparameters_tree = ET.parse(runparameters_path)
    global runparameters
    runparameters = runparameters_tree.getroot()


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
