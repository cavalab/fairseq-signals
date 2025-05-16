#!/bin/bash
# Sample batchscript to run a parallel python job on HPC using 10 CPU cores
#SBATCH --partition=gpu-chip-lacava     # queue to be used
#SBATCH --account=chip-lacava             # queue to be used
#SBATCH --qos=unlimited             # queue to be used
#SBATCH --time=02-00:00:00             # Running time (in days-hours:minutes:seconds)
#SBATCH --job-name=prep_bch             # Job name
#SBATCH --output=%j.out          # Name of the output file
#SBATCH --nodes=1               # Number of compute nodes
#SBATCH --ntasks=1             #
#SBATCH --cpus-per-task=64  #Number of cpu cores on one node
#SBATCH --mem=256G
 

LABSHARE="/lab-share/CHIP-Lacava-e2/Groups/BCH-Cardio/" 
PROCESSED_ROOT="${LABSHARE}/fairseq-processed/data"
SCRIPTS="scripts/preprocess/ecg"

BCH_ROOT="${LABSHARE}/All_ECGs/"

# No need for a code_15_records.py script
# Simply rename exams.csv to records.csv and place it in the processed root
mkdir -p "${PROCESSED_ROOT}/bch/"

echo "bch_records.py"
python -u ${SCRIPTS}/bch_records.py \
    --processed_root "$PROCESSED_ROOT/bch" \
    --raw_root "$BCH_ROOT" \

python -u ${SCRIPTS}/bch_signals.py --help

python -u ${SCRIPTS}/bch_signals.py \
    --processed_root "$PROCESSED_ROOT/bch" \
    --raw_root "$BCH_ROOT/" \
    --manifest_file "$PROCESSED_ROOT/manifest.csv" 
    
# echo "splits.py"
# python ${SCRIPTS}/../splits.py \
#     --strategy "grouped" \
#     --processed_root "$PROCESSED_ROOT/bch" \
#     --group_col "subject_id" \
#     --filter_cols "nan_any,constant_leads_any"

# TODO: separate label generation for each outcome
