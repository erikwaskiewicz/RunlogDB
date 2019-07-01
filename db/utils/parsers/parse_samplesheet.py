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


def format_section(header_section):
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




#---------------------------------------------------------------------------
def extract_description_data(data_section):
    """
    take a dataframe of the data section and split out the items in the 
    description field into individual columns
    """
    # open empty df to save description field items to
    desc_df = pd.DataFrame()
    # loop through each row in the data_Section df
    for sample in data_section.Sample_ID:

        # subset the data to only include the sample row
        subset = data_section[data_section.Sample_ID == sample]
        # make an df for the row data with sample ID for merging later on
        temp_df = pd.DataFrame(data={'Sample_ID': [ sample ]})

        # split the description field into its key-value pairs and loop through
        desc = subset.Description.values[0].split(';')
        for i in desc:
            # split the key-value pair, add to df - key is column name, value is record
            try:
                desc_split = i.split('=')
                temp_df[desc_split[0]] = [desc_split[1]]
            except IndexError:
                pass
        # append the temp df onto the main description field df
        desc_df = desc_df.append(temp_df, ignore_index=True, sort=False)
    
    # merge
    data_section_out = pd.merge(data_section, desc_df, on='Sample_ID')
    data_section_out = data_section_out.set_index('Sample_ID')

    return data_section_out


def make_data_section_dict(worksheets, data_section):
    """
    Take the data section dictionary after the descriptions have been included and 
    format it into a dictionary
    """
    data_dict = {}
    for worksheet in worksheets:

        subset = data_section[data_section.Sample_Plate == worksheet]

        assert len(subset.Sample_Plate.unique()) == 1
        assert len(subset.panel.unique()) == 1
        assert len(subset.pipelineName.unique()) == 1
        assert len(subset.pipelineVersion.unique()) == 1

        # change NTC to NTC-worksheet_number
        subset.at['NTC', 'Sample_Name'] = f'NTC-{worksheet}' # change sample_name
        subset.rename(index={'NTC': f'NTC-{worksheet}'}, inplace=True) # change sample ID index

        # list values that are common to all samples, extract the variables
        ws_specific = ['Sample_Plate', 'panel', 'pipelineName', 'pipelineVersion']
        sample_plate = subset.Sample_Plate.unique()[0]
        pipeline_name = subset.pipelineName.unique()[0]
        pipeline_version = subset.pipelineVersion.unique()[0]
        panel = subset.panel.unique()[0]

        # extract sample specific info from df into json
        sample_specific_json = json.loads(subset.drop(ws_specific, axis=1).to_json(orient='index'))

        for s in sample_specific_json:
            # make sure there is always a sex field
            try:
                sample_specific_json[s]['sex']
            except KeyError:
                sample_specific_json[s]['sex'] = ''
            # reformat values to prevent downstream errors
            for key, value in sample_specific_json[s].items():
                if value == None:
                    sample_specific_json[s][key] = ''
                if key == 'sex':
                    if value == '1':
                        sample_specific_json[s][key] = 'M'
                    elif value == '2':
                        sample_specific_json[s][key] = 'F'

        # add to python dic with worksheet as the key
        data_dict[worksheet] = {
            'Sample_Plate': sample_plate,
            'pipelineName': pipeline_name,
            'pipelineVersion': pipeline_version,
            'panel': panel,
            'samples': sample_specific_json
            }
        
    return data_dict


def make_data_section_dict_nipt(worksheets, data_section, experiment_name):
    data_dict = {}
    for worksheet in worksheets:
        subset = data_section[data_section.Sample_Project == worksheet]
        assert len(subset.Sample_Project.unique()) == 1

        # extract sample specific info from df into json
        # TODO - rename NTC as NTC+WS??
        subset = subset.drop(subset[subset.Lane == '2'].index)
        ws_specific = ['Sample_Plate', 'Sample_Project']
        subset_processed = subset.drop(ws_specific, axis=1).set_index('Sample_ID')

        sample_specific_json = json.loads(subset_processed.to_json(orient='index'))

        for s in sample_specific_json:
            # make sure there is always a sex field
            try:
                sample_specific_json[s]['sex']
            except KeyError:
                sample_specific_json[s]['sex'] = ''
            # reformat values to prevent downstream errors
            for key, value in sample_specific_json[s].items():
                if value == None:
                    sample_specific_json[s][key] = ''

        if 'fail' in worksheet.lower():
            worksheet = f'{experiment_name}_Failed'
        # add to python dic with worksheet as the key
        data_dict[worksheet] = {
            'Sample_Project': subset.Sample_Project.unique()[0],
            'Sample_Plate': '',
            'pipelineName': '',
            'pipelineVersion': '',
            'panel': 'NIPT',
            'samples': sample_specific_json
            } # TODO - add other nipt fields to models?
        
    return data_dict



# ## Combine header, reads and data into JSON object

# loop through sections dict
# if header, reads or data sections, call relevant function
# else call generic function
# combine all dicts at the end and make json file
# return json file as string

def get_samplesheet_dict(run_folder, run_type=''):
    
    filename = get_samplesheet_path(run_folder)

    with open(os.path.abspath(filename)) as file:
        reader = csv.reader(file)
        samplesheet = list(reader)

    # get section line numbers
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
                    end = n+1
                section_line_nos[key] = [start, end]
                in_section = False


    assert 'Header' in section_line_nos
    assert 'Data' in section_line_nos

    # make dict of whole samplesheet
    combined_dict = {}
    for section in section_line_nos.keys():
        
        extract = extract_section(section_line_nos, section, samplesheet)

        if section == 'Header':
            if run_type == 'nipt':
                # swap experiment and investigator round in nipt
                extract_dict = format_section(extract)
                extract_dict['Experiment_Name'], extract_dict['Investigator_Name'] = extract_dict['Investigator_Name'], extract_dict['Experiment_Name']
            else:
                extract_dict = format_section(extract)
        elif section == 'Reads':
            extract_dict = format_reads_section(extract)
        elif section == 'Data':
            data_section = pd.DataFrame(extract[1:], columns=extract[0])

            if run_type == 'nipt':
                experiment_name = combined_dict['Header']['Experiment_Name']
                worksheets = data_section.Sample_Project.unique()
                extract_dict = make_data_section_dict_nipt(worksheets, data_section, experiment_name)
            else:
                data_section = extract_description_data(data_section)
                worksheets = data_section.Sample_Plate.unique()
                extract_dict = make_data_section_dict(worksheets, data_section)
        else:
            extract_dict = format_section(extract)

            # TODO add handling for other sections - make dict and add to combined dict
        combined_dict[section] = extract_dict

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
