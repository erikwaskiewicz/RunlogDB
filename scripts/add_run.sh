#!/bin/bash

# activate conda environment
source activate runlogdb-env

# assign run folder path from input
run_folder=$1

# add run
echo -e $(date) "\tAdding $run_folder"
python3.6 /data/diagnostics/apps/RunlogDB/RunlogDB-0.1.1/main.py $run_folder
echo "Done."
echo "----------------------------------------------------------------------------------------------------"

# deactivate conda environment
source deactivate
