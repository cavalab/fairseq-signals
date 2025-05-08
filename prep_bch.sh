#!/bin/bash
# Sample batchscript to run a parallel python job on HPC using 10 CPU cores
#SBATCH --partition=bch-compute             # queue to be used
#SBATCH --time=08:00:00             # Running time (in hours-minutes-seconds)
#SBATCH --job-name=prep_physionet             # Job name
#SBATCH --output=%j.out          # Name of the output file
#SBATCH --nodes=1               # Number of compute nodes
#SBATCH --ntasks=8             # Number of cpu cores on one node
 

LABSHARE="/rc-fs/chip-lacava/Groups/BCH-Cardio/" 
PROCESSED_ROOT="${LABSHARE}/fairseq-processed/data"
SCRIPTS="scripts/preprocess/ecg"

BCH_ROOT="${LABSHARE}/All_ECGs/"

# No need for a code_15_records.py script
# Simply rename exams.csv to records.csv and place it in the processed root
mkdir -p "${PROCESSED_ROOT}/bch/"
# cp "${CODE_15_ROOT}/exams.csv" "${PROCESSED_ROOT}/code_15/records.csv"

# echo "bch_records.py"
# python ${SCRIPTS}/bch_records.py \
#     --processed_root "$PROCESSED_ROOT/bch" \
#     --raw_root "$BCH_ROOT" \

python ${SCRIPTS}/bch_signals.py --help

python ${SCRIPTS}/bch_signals.py \
    --processed_root "$PROCESSED_ROOT/bch" \
    --raw_root "$BCH_ROOT/" \
    --manifest_file "$PROCESSED_ROOT/manifest.csv" \
    --no_parallel