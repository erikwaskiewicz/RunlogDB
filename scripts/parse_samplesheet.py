import csv
import itertools
import os.path


def get_variables(run_folder):
    """--- Get SampleSheet path ---
    Takes the run folder and looks for Samplesheet.csv in that folder. If found then sets the samplesheet path to the
    file, otherwise returns an error.
    """
    global samplesheet_path
    samplesheet_path = run_folder + r"/SampleSheet.csv"
    if os.path.isfile(samplesheet_path) is False:
        print("\tCould not open file", samplesheet_path)


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
        # Currently don't have a better identifier for NIPT
        elif "cfDNA" in var:
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
