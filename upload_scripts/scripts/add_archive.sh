#!/bin/bash

# activate conda environment
source activate runlogdb-env

# hiseq
for run_folder in ~/Documents/archive/miseq/*
do
    echo -e $(date) "\tAdding $run_folder"
    python3.6 ~/Projects/RunlogDB/main.py $run_folder
    echo "Done."
    echo "----------------------------------------------------------------------------------------------------"
done

# miseq
for run_folder in ~/Documents/archive/hiseq/*
do
    echo -e $(date) "\tAdding $run_folder"
    python3.6 ~/Projects/RunlogDB/main.py $run_folder
    echo "Done."
    echo "----------------------------------------------------------------------------------------------------"
done

# NIPT
#for run_folder in /data/archive/nipt/runs/*
#do
#    echo -e $(date) "\tAdding $run_folder"
#    python3.6 /data/diagnostics/apps/RunlogDB/main.py $run_folder
#    echo "Done."
#    echo "----------------------------------------------------------------------------------------------------"
#done

# deactivate conda environment
source deactivate
