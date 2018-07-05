#!/bin/bash

# activate conda environment
source activate runlogdb-env

# assign run folder path from input
run_folder=$1

# add run
echo -e $(date) "\tAdding $run_folder"
python3.6 /data/diagnostics/apps/RunlogDB/main.py $run_folder
echo "Done."
echo "----------------------------------------------------------------------------------------------------"

# deactivate conda environment
source deactivate
