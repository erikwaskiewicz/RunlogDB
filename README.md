# RunlogDB

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


## Potential errors
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
