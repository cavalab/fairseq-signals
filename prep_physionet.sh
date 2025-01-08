#!/bin/bash
LABSHARE="/media/drive2/cavalab/data/Public" 
PROCESSED_ROOT="${LABSHARE}/fairseq-processed/data"
PHYSIONET_ROOT="${LABSHARE}/physionet.org/files/challenge-2021/1.0.3/training/"
EVALUATION_ROOT="${LABSHARE}/physionetchallenges/evaluation-2021"

SCRIPTS="scripts/preprocess/ecg"

echo "python ${SCRIPTS}/physionet2021_records.py"

python ${SCRIPTS}/physionet2021_records.py \
    --processed_root "$PROCESSED_ROOT/physionet2021/" \
    --raw_root "$PHYSIONET_ROOT"


clear
python ${SCRIPTS}/physionet2021_signals.py --help

echo "python ${SCRIPTS}/physionet2021_signals.py" 

python ${SCRIPTS}/physionet2021_signals.py \
    --processed_root "$PROCESSED_ROOT/physionet2021/" \
    --raw_root "$PHYSIONET_ROOT" \
    --manifest_file "$PROCESSED_ROOT/manifest.csv" \
    --nb_workers 120

clear
echo "python ${SCRIPTS}/../splits.py" 

python ${SCRIPTS}/../splits.py \
    --strategy "random" \
    --processed_root "$PROCESSED_ROOT/physionet2021/" \
    --filter_cols "nan_any,constant_leads_any" \
    --dataset_subset "cpsc_2018, cpsc_2018_extra, georgia, ptb-xl, chapman_shaoxing, ningbo" # Excludes 'ptb' and 'st_petersburg_incart'

mkdir $PROCESSED_ROOT/physionet2021/labels
# clear
echo "python ${SCRIPTS}/physionet2021_labels.py" 

python ${SCRIPTS}/physionet2021_labels.py \
    --processed_root "$PROCESSED_ROOT/physionet2021/" \
    --weights_path "$EVALUATION_ROOT/weights.csv" \
    --weight_abbrev_path "$EVALUATION_ROOT/weights_abbreviations.csv" 

# clear
echo "python ${SCRIPTS}/../prepare_clf_labels.py" 

python ${SCRIPTS}/../prepare_clf_labels.py \
    --output_dir "$PROCESSED_ROOT/physionet2021/labels" \
    --labels "$PROCESSED_ROOT/physionet2021/labels/labels.csv" \
    --meta_splits "$PROCESSED_ROOT/physionet2021/meta_split.csv"
