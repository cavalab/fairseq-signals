"""Record extraction code for BCH."""

import os
import argparse

import pandas as pd


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


def main(args):
    """
    Main processing function that combines and manipulates multiple datasets.

    Parameters
    ----------
    args : argparse.Namespace
        Command line arguments.
    """
    os.makedirs(args.processed_root, exist_ok=True)

    records_file = os.path.join(args.raw_root, "RECORDS_all.txt")
    train_records_file = os.path.join(args.raw_root, "RECORDS_train.txt")
    print(f"reading {records_file}")
    with open(records_file, "r") as rf:
        records = [r.strip() for r in rf.readlines()]
    print(f"reading {train_records_file}")
    with open(train_records_file, "r") as rf:
        train_records = [r.strip() for r in rf.readlines()]
    print('generating fold...')
    fold = ['train' if ecg_id in train_records else 'test' for ecg_id in records]
    records_df = pd.DataFrame(
        {"ecg_id": records, 
        "path": "all_ECGs_float32_T_grouped.h5",
        'fold': fold
        }
    )
    filename = "records"
    print(f"writing {filename}.csv")
    records_df.to_csv(os.path.join(args.processed_root, f"{filename}.csv"), index=False)


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args)
