#!/bin/bash
# Sample batchscript to run a parallel python job on HPC using 10 CPU cores
 
#SBATCH --partition=bch-compute             # queue to be used
#SBATCH --time=08:00:00             # Running time (in hours-minutes-seconds)
#SBATCH --job-name=prep_ptbxl             # Job name
#SBATCH --output=%j.out          # Name of the output file
#SBATCH --nodes=1               # Number of compute nodes
#SBATCH --ntasks=1             # Number of cpu cores on one node
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
LABSHARE='/media/drive2/cavalab/data/Public' 
python fairseq_signals/data/ecg/preprocess/preprocess_ptbxl.py \
    "${LABSHARE}/physionet.org/files/ptb-xl/1.0.3/records500/"  \
    --dest ~/labshare/Public/fairseq-preprocess/data/ptbxl/ \