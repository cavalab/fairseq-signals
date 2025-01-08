#!/bin/bash
set -e
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

MIMIC_IV_ECG_ROOT="${LABSHARE}/physionet.org/files/mimic-iv-ecg/1.0/"
MIMIC_IV_ROOT="${LABSHARE}/physionet.org/files/mimiciv/2.2/" # Optional

echo "mimic_iv_ecg_records.py"
python ${SCRIPTS}/mimic_iv_ecg_records.py \
    --processed_root "$PROCESSED_ROOT/mimic_iv_ecg" \
    --raw_root "$MIMIC_IV_ECG_ROOT" \
    --mimic_iv_root "$MIMIC_IV_ROOT" # Optional

clear
echo "signals.py"
python ${SCRIPTS}/mimic_iv_ecg_signals.py --help

python ${SCRIPTS}/mimic_iv_ecg_signals.py \
    --processed_root "$PROCESSED_ROOT/mimic_iv_ecg" \
    --raw_root "$MIMIC_IV_ECG_ROOT" \
    --manifest_file "$PROCESSED_ROOT/manifest.csv"

clear 
echo "splits.py"
python ${SCRIPTS}/../splits.py \
    --strategy "grouped" \
    --processed_root "$PROCESSED_ROOT/mimic_iv_ecg" \
    --group_col "subject_id" \
    --filter_cols "nan_any,constant_leads_any"