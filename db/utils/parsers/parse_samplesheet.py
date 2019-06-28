import csv
import itertools
import os.path
import os
import sys
import csv
import pandas as pd
import json


### Load file
def get_samplesheet_path(run_folder):
    """--- Get SampleSheet path ---
    Takes the run folder and looks for Samplesheet.csv in that folder. If found then sets the samplesheet path to the
    file, otherwise returns an error.
    """
    samplesheet_path = run_folder + r"/SampleSheet.csv"
    if os.path.isfile(samplesheet_path) is False:
        print("\tCould not open file", samplesheet_path)

    return samplesheet_path


### Function to extract each section from the whole list
def extract_section(section_dict, section, samplesheet):
    """
    input
      section_dict - a dictionary with the section name as a key and [start, end] as the value
      section - String of the section to be extracted
    output
      extracted_section
    """
    start = section_dict[section][0]
    end = section_dict[section][1]

    extracted_section = samplesheet[start:end]
    return extracted_section


def format_header_section(header_section):
    header_dict = {}

    for item in header_section:
        key = item[0].replace(' ', '_')
        value = item[1]

        header_dict[key] = value
        
    return header_dict


def format_reads_section(reads_section):
    reads_dict = {}

    for n, item in enumerate(reads_section):
        key = 'read{}'.format(n+1)
        value = item[0]

        reads_dict[key] = value
    
    return reads_dict


def extract_description_data(data_section):
    # open empty df to save description field items to
    desc_df = pd.DataFrame()

    # loop through each row in the data_Section df
    for sample in data_section.Sample_ID:

        # subset the data to only include the sample row
        subset = data_section[data_section.Sample_ID == sample]

        # make an empty df for the row data
        temp_df = pd.DataFrame()

        # split the description field into its key-value pairs and loop through
        desc = subset.Description.values[0].split(';')
        for i in desc:

            # save sample ID for merging later on
            temp_df['Sample_ID'] = sample

            # split the key-value pair, add to df - key is column name, value is record
            desc_split = i.split('=')
            temp_df[desc_split[0]] = [desc_split[1]]

        # append the temp df onto the main description field df
        desc_df = desc_df.append(temp_df, ignore_index=True, sort=False)
        
    return desc_df


def merge_description_data(data_section, desc_df):
    data_section = pd.merge(data_section, desc_df, on='Sample_ID')
    data_section = data_section.set_index('Sample_ID')
    
    return data_section


def make_data_section_dict(worksheets, data_section):
    data_dict = {}
    for worksheet in worksheets:
        subset = data_section[data_section.Sample_Plate == worksheet]

        assert len(subset.Sample_Plate.unique()) == 1
        assert len(subset.panel.unique()) == 1
        assert len(subset.pipelineName.unique()) == 1
        assert len(subset.pipelineVersion.unique()) == 1

        # list values that are common to all samples, extract the variables
        ws_specific = ['Sample_Plate', 'panel', 'pipelineName', 'pipelineVersion']
        sample_plate = subset.Sample_Plate.unique()[0]
        pipeline_name = subset.pipelineName.unique()[0]
        pipeline_version = subset.pipelineVersion.unique()[0]
        panel = subset.panel.unique()[0]

        # extract sample specific info from df into json
        sample_specific_json = json.loads(subset.drop(ws_specific, axis=1).to_json(orient='index'))

        # add to python dic with worksheet as the key
        data_dict[worksheet] = {
            'Sample_Plate': sample_plate,
            'pipelineName': pipeline_name,
            'pipelineVersion': pipeline_version,
            'panel': panel,
            'samples': sample_specific_json
            }
        
    return data_dict


def format_data_reads(data_section):
    data_section = pd.DataFrame(data_section[1:], columns=data_section[0])
    desc_df = extract_description_data(data_section)
    data_section = merge_description_data(data_section, desc_df)
    worksheets = data_section.Sample_Plate.unique()
    data_dict = make_data_section_dict(worksheets, data_section)
    
    return data_dict


# ---

# ## Combine header, reads and data into JSON object

# --- 
# 
# ## Script


# loop through sections dict
# if header, reads or data sections, call relevant function
# else call generic function
# combine all dicts at the end and make json file
# return json file as string

def get_samplesheet_dict(run_folder):
    
    filename = get_samplesheet_path(run_folder)

    with open(os.path.abspath(filename)) as file:
        reader = csv.reader(file)
        samplesheet = list(reader)

    no_of_lines = len(samplesheet)
    section_line_nos = {}
    in_section = False

    for n, line in enumerate(samplesheet):
        if in_section == False:
            if line[0].startswith('[') and line[0].endswith(']'):
                key = line[0].strip('[]')
                start = n + 1
                in_section = True
        if in_section == True:
            if line[0] == '' or n == (no_of_lines - 1):
                if line[0] == '':
                    end = n
                if n == (no_of_lines - 1):
                    end = n
                section_line_nos[key] = [start, end]
                in_section = False


    assert 'Header' in section_line_nos
    assert 'Data' in section_line_nos

    combined_dict = {}
    for section in section_line_nos.keys():
        extract = extract_section(section_line_nos, section, samplesheet)
        if section == 'Header':
            extract_dict = format_header_section(extract)
        if section == 'Reads':
            extract_dict = format_reads_section(extract)
        if section == 'Data':
            extract_dict = format_data_reads(extract)
        else:
            pass
            # add other bit here
        combined_dict[section] = extract_dict

    return combined_dict
    #combined_json_output = json.dumps(combined_dict, indent=2, separators=(',', ':'))
    #print(combined_json_output)




def extract_data(samplesheet_dict):
    samplesheet_sorted = {}

    try: samplesheet_sorted['investigator'] = samplesheet_dict['Header']['Investigator_Name']
    except KeyError: samplesheet_sorted['investigator'] = ''
    try: samplesheet_sorted['experiment'] = samplesheet_dict['Header']['Experiment_Name']
    except KeyError: samplesheet_sorted['experiment'] = ''
    try: samplesheet_sorted['samplesheet_date'] = samplesheet_dict['Header']['Date']
    except KeyError: samplesheet_sorted['samplesheet_date'] = ''
    try: samplesheet_sorted['workflow'] = samplesheet_dict['Header']['Workflow']
    except KeyError: samplesheet_sorted['workflow'] = ''
    try: samplesheet_sorted['application'] = samplesheet_dict['Header']['Application']
    except KeyError: samplesheet_sorted['application'] = ''
    try: samplesheet_sorted['assay'] = samplesheet_dict['Header']['Assay']
    except KeyError: samplesheet_sorted['assay'] = ''
    try: samplesheet_sorted['chemistry'] = samplesheet_dict['Header']['Chemistry']
    except KeyError: samplesheet_sorted['chemistry'] = ''
    try: samplesheet_sorted['description'] = samplesheet_dict['Header']['Description']
    except KeyError: samplesheet_sorted['description'] = ''

    return samplesheet_sorted




'''
# Define parse_samplesheet function for parsing general SampleSheet data
def parse1(run_folder, dictionary, samplesheet_value):
    """--- Parse SampleSheet data 1 ---
    Parses the [header] section of SampleSheet.csv, takes a variable, looks for it in column 1, if it finds the variable
    then returns the value in column 2. If the variable is not found then returns Null.
    """
    get_variables(run_folder)
    content = "Null"
    with open(samplesheet_path, newline="") as ss_csv:
        ss = csv.reader(ss_csv, delimiter=",")
        for row in ss:
            if any(row):
                if row[0] == samplesheet_value:
                    content = row[1]
                    if content == "":
                        content = "Null"
        dictionary[samplesheet_value] = content


def parse2(run_folder, dictionary, variable, header):
    """--- Parse SampleSheet data 2 ---
    Parses the [data] table in SampleSheet.csv, takes a header from the table and returns a list of unique values within
    that column, separated by a comma.

    Steps:
      - Loads csv file
      - Loops through each row to find the row containing the header
      - Loops through that row to find the column containing the header
      - Extract the whole column into an array
      - Loops through the array and save each unique entry to a new array
      - Output the unique array as a string seperated by commas and add to dictionary

    parse_samplesheet.parse2 is used to extract data from the 'Plates' column, which usually contains worksheet IDs, and
    the 'Description' column, which ususally contains the pipeline information. For the Description column, panel names
    are extracted and renamed appropriately (see code for details).
    """
    get_variables(run_folder)
    var_list = []
    var_str = ""

    # Load csv file and count total number of rows
    with open(samplesheet_path, newline="") as samplesheet_csv:
        samplesheet = csv.reader(samplesheet_csv, delimiter=",")
        row_count = sum(1 for row in samplesheet)

    # Find first row of table containing header and then find header column
    start_row = row_count
    with open(samplesheet_path, newline="") as samplesheet_csv:
        samplesheet = csv.reader(samplesheet_csv, delimiter=",")
        for count1, row in enumerate(samplesheet):
            if any(row):
                if header in row:
                    start_row = count1
                    for count2, col in enumerate(row):
                        if col == header:
                            start_col = count2

    # Extract header column from table to var_list array
    with open(samplesheet_path, newline="") as samplesheet_csv:
        samplesheet = csv.reader(samplesheet_csv, delimiter=",")
        for row in itertools.islice(samplesheet, start_row + 1, row_count):
            var_list.append(row[start_col])

    # Make array containing a list of unique values from var_array
    var_unique = []
    for var in var_list:
        if var not in var_unique:
            var_unique.append(var)
        if var == "":
            var_unique.remove(var)

    # Concatenate list of unique values into a string, rename to "Null" if list is empty. Add result to dictionary.
    var_unique = sorted(var_unique)
    for var in var_unique:
        var_str += str(var) + ", "
    if var_str == "":
        var_str = "Null"
    dictionary[variable] = var_str.rstrip(', ')


def parse3(dictionary):
    # Rename pipeline names to something more meaningful -- For 'Description' column only.
    # This will work on data from all columns but it is unlikely that these variables will appear in them, and it
    # shouldn't matter if they do.
    # Add panel information here if new panels added
    var_list = dictionary["Description2"].split(',')
    out_list = []
    out_str = ""
    for var in var_list:
        if "NGHS-101X-WCB" in var:
            out_list += ["WCB"]
        elif "NGHS-101X" in var:
            out_list += ["CRM"]
        elif "NGHS-102X" in var:
            out_list += ["BRCA"]
        elif "CRUK" in var:
            out_list += ["CRUK"]
        elif "TruSightCancer" in var:
            out_list += ["TruSightCancer"]
        elif "TruSightOne" in var:
            out_list += ["TruSightOne"]
        elif "NGHS-201X" in var:
            out_list += ["TAM"]
        elif "TruSightMyeloid" in var:
            out_list += ["TruSightMyeloid"]
        elif "RochePanCancer" in var:
            out_list += ["RochePanCancer"]
        # Currently don't have a better identifier for NIPT
        elif "cfDNA" in dictionary["Description"]:
            out_list += ["NIPT"]
            experiment = dictionary["Experiment Name"]
            investigator = dictionary["Investigator Name"]
            dictionary["Experiment Name"] = investigator
            dictionary["Investigator Name"] = experiment

    # Make array containing a list of unique values from var_array
    var_unique = []
    for var in out_list:
        if var not in var_unique:
            var_unique.append(var)
        if var == "":
            var_unique.remove(var)

    # Concatenate list of unique values into a string, rename to "Null" if list is empty. Add result to dictionary.
    var_unique = sorted(var_unique)
    for var in var_unique:
        out_str += str(var) + ", "
    if out_str == "":
        out_str = "Null"
    dictionary["Pipeline"] = out_str.rstrip(', ')

    return dictionary
'''