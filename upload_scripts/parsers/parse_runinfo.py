import os.path
from datetime import date
import xml.etree.ElementTree as ET


def get_variables(run_folder):
    runinfo_path = run_folder + r"/RunInfo.xml"
    if os.path.isfile(runinfo_path) is False:
        exit("ERROR  Could not open file " + runinfo_path)
    runinfo_tree = ET.parse(runinfo_path)
    runinfo = runinfo_tree.getroot()
    return runinfo


def parse1(run_folder, dictionary, runinfo_value, value_type):
    """Parses data within RunInfo.xml file. Data must be within the terms RunInfo>Run.
       get retrieves data within an xml header, find retrieves data within between the xml headers."""
    runinfo = get_variables(run_folder)
    for runinfo_parameter in runinfo.iter("Run"):
        if runinfo_value == "Date":
            if runinfo_parameter.find(runinfo_value) is not None:
                d = str(runinfo_parameter.find(runinfo_value).text)
                year = '20' + d[0:2]
                month = d[2:4]
                day = d[4:6]
                dictionary[runinfo_value] = date(int(year), int(month), int(day)).isoformat()
            else:
                dictionary[runinfo_value] = "Null"
        else:
            if value_type == "get":
                if runinfo_parameter.get(runinfo_value) is not None:
                    dictionary[runinfo_value] = runinfo_parameter.get(runinfo_value)
                else:
                    dictionary[runinfo_value] = "Null"
            if value_type == "find":
                if runinfo_parameter.find(runinfo_value) is not None:
                    dictionary[runinfo_value] = runinfo_parameter.find(runinfo_value).text
                else:
                    dictionary[runinfo_value] = "Null"


def parse2(run_folder, dictionary):
    get_variables(run_folder)
    reads_array = []
    for parameter in runinfo.iter("Run"):
        for reads in parameter.find("Reads"):
            if reads.get("IsIndexedRead") == "N":
                reads_array.append(reads.get("NumCycles"))
        if len(reads_array) < 2:
            reads_array.append("Null")
        dictionary["num_cycles1"] = reads_array[0]
        dictionary["num_cycles2"] = reads_array[1]
