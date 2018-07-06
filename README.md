# RunlogDB

Database to record parameters from NGS runs as they come off the machines. It consists of a Django app with a SQLite3 backend 
and a simple HTML/ Bootstrap frontend to be used for querying the data. Data is uploaded by a seperate Python script, main.py.  

Currently the only querying possible is a simple search function and a query to download a spreadsheet containing the data 
necessary for producing the monthly NGS KPIs (setup date and run date, split by pipeline). There is a lot of scope to develop 
new features for the frontend.  

This database was a project for my STP Computing for Clinical Scientists (SBI101) rotation.

## Parameters

The database is split into three tables:
- Runlog: data common to all sequencing runs, regardless of instrument type.
  - Run ID, worksheet ID, panels, sample IDs
  - Setup and run dates
  - QC metrics - interops and sensitivity data
  - Other data pulled from the samplesheet
- Miseq/Hiseq/Nextseq tables: data specific to the relevent instrument.
  - Specific data about the sequencer settings 
  - Pulled from the RunParameters.xml file

## Setup
- Copy over whole directory
- Create conda ennvironment from yaml file
  - ```conda env create -f runlogdb-env.yml```
  - activate the new environment - ```source activate runlogdb-env```
  - check that environment installed correctly - ```conda list```
- create new database - ```python manage.py migrate```
- change filepaths to point to this database
  - ```scripts/add_to_db.py```
  - ```scripts/print.sh```
- change filepaths to point to main.py
  - ```scripts/add_run.sh```
  - ```scripts/add_nipt.sh```
  - ```scripts/add_archive.sh```
- run add_archive to add all previous runs
  - some runs will throw errors, see file for details
- add commands in ```scripts/cron.sh``` to cron job to find and add any further runs as they are made
- host frontend on cluster usign apache - TO DO

### Directory structure
```bash
RunlogDB
|-- runlog
|   |-- db
|   |-- runlog
|   |-- manage.py
|   |-- runlogdb.sqlite3
|-- scripts
|   |-- __pycache__
|   |-- add_archive.sh
|   |-- add_nipt.sh
|-- main.py
|-- README.md
|-- runlog_upload_log.txt
|-- runlogdb-env.yml
```

## Potential upload errors
There are some common errors when upaloding a run to the database, they are shown below.
Most commly it is either the samplesheet has been setup incorrectly or the run failed, 
meaning that the required files aren't present.

- ERROR 1: run failed/ not organised in usual way
```bash
ERROR  Could not open file /data/archive/miseq/161215_M00766_0104_000000000-AVB1R/RunInfo.xml
```

- ERROR 2: no interops files - either failed run or different folder layout
```bash
Traceback (most recent call last):
  File "/data/diagnostics/apps/RunlogDB/main.py", line 59, in <module>
    parse_interop.parse(run_folder, interop_dict)
  File "/state/partition1/data/diagnostics/apps/RunlogDB/scripts/parse_interop.py", line 13, in parse
    dictionary["Cluster density"] = round(summary.at(0).at(0).density().mean() / 1000, 2)
  File "/share/apps/anaconda2/envs/runlogdb-env/lib/python3.6/site-packages/interop/py_interop_summary.py", line 483, in at
    return _py_interop_summary.run_summary_at(self, n)
interop.py_interop_metrics.index_out_of_bounds_exception: Read index exceeds read count - 0 >= 0
/io/./interop/model/summary/run_summary.h::operator[] (181)
```

- ERROR 3: trailing comma missing from [header] section of sample sheet
```bash
Traceback (most recent call last):
  File "/data/diagnostics/apps/RunlogDB/main.py", line 45, in <module>
    parse_samplesheet.parse1(run_folder, samplesheet_dict, value)
  File "/state/partition1/data/diagnostics/apps/RunlogDB/scripts/parse_samplesheet.py", line 30, in parse1
    content = row[1]
IndexError: list index out of range
```

- ERROR 4: trailing commas missing in sample sheet [data] table
```bash
Traceback (most recent call last):
  File "/data/diagnostics/apps/RunlogDB/main.py", line 49, in <module>
    parse_samplesheet.parse2(run_folder, samplesheet_dict, "Pipeline", "Description")
  File "/state/partition1/data/diagnostics/apps/RunlogDB/scripts/parse_samplesheet.py", line 78, in parse2
    var_list.append(row[start_col])
IndexError: list index out of range
```
