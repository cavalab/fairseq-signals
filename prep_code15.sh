#!/bin/bash
# Sample batchscript to run a parallel python job on HPC using 10 CPU cores
 
#SBATCH --partition=bch-compute             # queue to be used
#SBATCH --time=08:00:00             # Running time (in hours-minutes-seconds)
#SBATCH --job-name=prep_physionet             # Job name
#SBATCH --output=%j.out          # Name of the output file
#SBATCH --nodes=1               # Number of compute nodes
#SBATCH --ntasks=8             # Number of cpu cores on one node
 

LABSHARE="/media/drive2/cavalab/data/Public" 
PROCESSED_ROOT="${LABSHARE}/fairseq-processed/data"
SCRIPTS="scripts/preprocess/ecg"

CODE_15_ROOT="${LABSHARE}/Code15"

# No need for a code_15_records.py script
# Simply rename exams.csv to records.csv and place it in the processed root
mkdir -p "${PROCESSED_ROOT}/code_15/"
cp "${CODE_15_ROOT}/exams.csv" "${PROCESSED_ROOT}/code_15/records.csv"

python ${SCRIPTS}/code_15_signals.py --help

python ${SCRIPTS}/code_15_signals.py \
    --processed_root "$PROCESSED_ROOT/code_15" \
    --raw_root "$CODE_15_ROOT/TRAIN" \
    --manifest_file "$PROCESSED_ROOT/manifest.csv"