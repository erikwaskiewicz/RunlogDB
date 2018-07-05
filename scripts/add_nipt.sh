#!/bin/bash

# activate conda environment
source activate runlogdb-env

# get most recent nipt run id and trim to get the date of the most recent nipt run uploaded
NIPT_RUNS=$(sqlite3 ./runlog/runlogdb.sqlite3 "SELECT run_id FROM db_runlog WHERE pipeline = 'NIPT' ORDER BY run_id DESC")
MOST_RECENT=$(echo $NIPT_RUNS | cut -d" " -f1 | cut -d"_" -f1)

# loop through nipt runs folder and add any runs with a date greater than the most recently added nipt run
# first if clause in to prevent printing error messages for folders in the run folder which aren't actually runs
for filepath in /data/archive/nipt/runs/*/; 
do
    RUN_DATE=$(basename $filepath | cut -d"_" -f1)
    if [ $? -eq 0 ] && [[ $RUN_DATE =~ ^[0-9]+$ ]]
    then
        if [ $RUN_DATE -gt $MOST_RECENT ]
        then
            echo -e $(date) "\tAdding $filepath"
            python3.6 /data/diagnostics/apps/RunlogDB/main.py $filepath
            echo "Done."
            echo "----------------------------------------------------------------------------------------------------"
        fi
    fi
done

# deactivate conda environment
source deactivate
