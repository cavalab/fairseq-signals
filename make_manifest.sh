#!/bin/bash
LABSHARE="/media/drive2/cavalab/data/Public" 
PROCESSED_ROOT="${LABSHARE}/fairseq-processed/data"
MANIFEST_DIR="$PROCESSED_ROOT/manifests/physionet2021/"
mkdir -p $MANIFEST_DIR

# cd .../fairseq-signals/scripts/preprocess
SCRIPTS="scripts/preprocess/"

python ${SCRIPTS}/manifests.py \
    --split_file_paths "$PROCESSED_ROOT/physionet2021/segmented_split.csv" \
    --save_dir "$MANIFEST_DIR"

# If training a CMSC model, the manifest must be converted accordingly
python fairseq_signals/data/ecg/preprocess/convert_to_cmsc_manifest.py \
    "$MANIFEST_DIR" \
    --dest "$MANIFEST_DIR"