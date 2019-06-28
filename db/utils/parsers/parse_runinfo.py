import os.path
from datetime import date
import xmltodict
import json



def get_runinfo_dict(run_folder):
    # make path to runinfo file
    runinfo_path = run_folder + r"/RunInfo.xml" # TODO use path package
    # check that file exists
    if os.path.isfile(runinfo_path) is False:
        exit(f"ERROR  Could not open file {runinfo_path}") # TODO add logging
    # turn XML file into a dictionary
    with open(runinfo_path) as f:
        runinfo_dict = xmltodict.parse(f.read())

    return runinfo_dict


def extract_data(runinfo_dict):
    """
    """
    # parse simple variables from xml dict
    runinfo_sorted_dict = {
        'run_id': runinfo_dict['RunInfo']['Run']['@Id'],   #@ == attribute
        'instrument': runinfo_dict['RunInfo']['Run']['Instrument'],
        'instrument_date': runinfo_dict['RunInfo']['Run']['Date']   #TODO make date object
    }
    
    # parse reads from xml dict and sort data
    reads = runinfo_dict['RunInfo']['Run']['Reads']['Read']
    num_reads = num_indexes = 0
    for r in reads:
        if r['@IsIndexedRead'] == 'Y':
            num_indexes += 1
            if num_indexes == 1:
                runinfo_sorted_dict['length_index1'] = r['@NumCycles']
            if num_indexes == 2:
                runinfo_sorted_dict['length_index1'] = r['@NumCycles']
        if r['@IsIndexedRead'] == 'N':
            num_reads += 1
            if num_reads == 1:
                runinfo_sorted_dict['length_read1'] = r['@NumCycles']
            if num_reads == 2:
                runinfo_sorted_dict['length_read1'] = r['@NumCycles']
    runinfo_sorted_dict['num_reads'] = num_reads
    runinfo_sorted_dict['num_indexes'] = num_indexes

    # encode xml dict as a json string
    runinfo_sorted_dict['raw_runinfo_json'] = json.dumps(runinfo_dict, indent=2, separators=(',', ':'))

    return runinfo_sorted_dict










'''
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
'''