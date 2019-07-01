import csv
import os
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
        print("\tCould not open file", samplesheet_path) #TODO add logging

    return samplesheet_path


def extract_section(section_dict, section, samplesheet):
    """
    Function to extract each section from the whole list

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
        if len(desc) > 1:
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


def sort_samplesheet_sex(samplesheet_dict):
    for ws in samplesheet_dict['Data']:
        ws_dict = samplesheet_dict['Data'][ws]
        for sample in ws_dict['samples']:
            sample_dict = ws_dict['samples'][sample]
            try:
                if sample_dict['sex'] == '1':
                    sex = 'M'
                elif sample_dict['sex'] == '2':
                    sex = 'F'
                else:
                    sex = ''
            except KeyError:
                sex = ''
            samplesheet_dict['Data'][ws]['samples'][sample]['sex'] = sex

    return samplesheet_dict


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

    combined_dict = sort_samplesheet_sex(combined_dict)

    return combined_dict


def extract_data(samplesheet_dict):
    """
    Extract run level data from the samplesheet dict so that it can be added to the 
    run level dict later on.
    If any values are missing, they will be set as an empty string. 
    """
    samplesheet_sorted = {}

    try: samplesheet_sorted['investigator'] = samplesheet_dict['Header']['Investigator_Name']
    except KeyError: samplesheet_sorted['investigator'] = ''
    try: samplesheet_sorted['experiment'] = samplesheet_dict['Header']['Experiment_Name']
    except KeyError: samplesheet_sorted['experiment'] = ''

    try:
        ss_date = samplesheet_dict['Header']['Date'] # TODO - check name of date field in ss generator
        year = ss_date.split('/')[2]
        month = ss_date.split('/')[1]
        day = ss_date.split('/')[0]
        samplesheet_sorted['samplesheet_date'] = date(int(year), int(month), int(day)).isoformat()
    except: 
        samplesheet_sorted['samplesheet_date'] = None

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


def sort_nipt_data(samplesheet_dict):
    """
    Sort the samplesheet dictionary to account for NIPT runs.
    NIPT samplesheets dont go through our usual samplesheet generator 
    so are in a different format to the others.
    """
    # there is no panel in the description field, set panel to NIPT
    print('nipt')
    #samplesheet_dict['panel'] = "NIPT" # TODO - panel is nested within ws - need to test wih NIPT samplesheet
    # experiment and investigator are switched in NIPT samplesheets, switch them round
    experiment = samplesheet_dict['Header']['Experiment_Name']
    investigator = samplesheet_dict['Header']['Investigator_Name']
    samplesheet_dict['Header']['Experiment_Name'] = investigator
    samplesheet_dict['Header']['Investigator_Name'] = experiment

    return samplesheet_dict
