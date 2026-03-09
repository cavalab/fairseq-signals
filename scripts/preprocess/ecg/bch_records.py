"""Record extraction code for BCH."""

import os

import pandas as pd
import numpy as np
import fire


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--processed_root",
        type=str,
        required=True,
        help="Directory to save the processed data.",
    )
    parser.add_argument(
        "--raw_root",
        type=str,
        required=True,
        help="Path to the raw data directory.",
    )

    return parser


def main(processed_root, raw_root, sample=None):
    """
    Main processing function that combines and manipulates multiple datasets.

    Parameters
    ----------
    processed_root: str
        Directory to save the processed data.
    raw_root: str
        Path to the raw data directory.
    sample: None or int
        If int, will sample records. Useful for debugging.
    """
    os.makedirs(processed_root, exist_ok=True)

    records_file = os.path.join(raw_root, "RECORDS_all.txt")
    print(f"reading {records_file}")
    with open(records_file, "r") as rf:
        records = np.array([r.strip() for r in rf.readlines()])

    train_records_file = os.path.join(raw_root, "RECORDS_train.txt")
    print(f"reading {train_records_file}")
    with open(train_records_file, "r") as rf:
        train_records = np.array([r.strip() for r in rf.readlines()])
    print('generating fold...')
    # https://numpy.org/doc/stable/reference/generated/numpy.in1d.html
    train_mask = np.isin(records,train_records,assume_unique=True)
    fold = ['train' if tm else 'test' for tm in train_mask] 
    fold = [f if f == 'test' else 'valid' if np.random.rand() < .1 else f for f in fold]
    records_df = pd.DataFrame(
        {"ecg_id": records, 
        "path": "all_ECGs_float32_T_grouped.h5",
        'pretrain_fold': fold
        }
    )
    if sample:
        records_df = records_df.sample(sample)
    filename = "records"
    print(f"writing {len(records_df)} records to {filename}.csv")
    records_df.to_csv(os.path.join(processed_root, f"{filename}.csv"), index=False)


if __name__ == "__main__":
    fire.Fire(main)