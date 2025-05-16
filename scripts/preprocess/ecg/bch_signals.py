"""Signal processing code example and guide."""

from typing import Union
import os
from scipy.io import savemat

import pandas as pd
import h5py

from preprocess import get_pipeline_parser, pipeline, reorder_leads, extract_feat_info

SOURCE = "BCH"


def extract_bch(
    row: pd.Series,
    leads_to_load: pd.DataFrame,
) -> Union[pd.Series, pd.DataFrame, dict]:
    """
    Extract ECG sample metadata and save a standardized .mat file.

    Parameters
    ----------
    row : pandas.Series
        Row of records data.
    leads_to_load : pandas.DataFrame
        Ordered leads to load which is used in the `reorder_leads` function.

    Return
    ------
    pandas.Series or pandas.DataFrame or dict of pandas.DataFrame
        A Series representing extracted metadata, or optionally a dictionary of
        Series/DataFrames which must contain a 'meta' entry.
    """
    ecg_file = row["path"]
    ecg_file = h5py.File(os.path.join(args.raw_root, ecg_file), "r")

    fields = {
        "sample_rate": 500  # Extract sample rate from the row or the file
    }
    # A NumPy array having shape (channels, sample size)
    feats = ecg_file[row["ecg_id"]][:]

    fields["sig_name"] = [
        "I",
        "II",
        "III",
        "aVR",
        "aVL",
        "aVF",
        "V1",
        "V2",
        "V3",
        "V4",
        "V5",
        "V6",
    ]  # A list of signal names representing the channel order
    # Must be a subset of: ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']

    # Re-order leads and handle missing
    feats, avail_leads = reorder_leads(feats, fields["sig_name"], leads_to_load)

    # Define and save a standard .mat file
    # Other information may be included, but these fields must be present
    fields = {
        "org_sample_rate": fields["sample_rate"],
        "curr_sample_rate": fields["sample_rate"],
        "org_sample_size": feats.shape[1],
        "curr_sample_size": feats.shape[1],
        "feats": feats,
        "idx": row["idx"],
    }
    savemat(row["save_path"], fields)

    fields["avail_leads"] = str(avail_leads)

    # Recommended to extract feature information on mean, STD, nulls, and constants
    fields.update(extract_feat_info(feats, leads_to_load))

    meta = pd.concat([
        pd.Series({
            "sample_rate": fields["org_sample_rate"],
            "sample_size": fields["org_sample_size"],
            "avail_leads": str(avail_leads),
        }),
        pd.Series(fields)
    ])

    return meta


def main(args):
    # Load the records
    records = pd.read_csv(os.path.join(args.processed_root, "records.csv"))

    # If the "path" column contains partial paths, the paths must be joined with the
    # raw data directory root
    records["path"] = records["path"].apply(lambda x: os.path.join(args.raw_root, x))

    # Turn file paths into unique file names
    # (Adding in the source string will ensure file names are unique across sources)
    records["save_file"] = records["ecg_id"].astype(str) + ".mat"

    records["source"] = SOURCE

    # Specify like so if source has one dataset, as this column must be present
    records["dataset"] = SOURCE

    pipeline(
        args,
        records,
        SOURCE,
        extract_func=extract_bch
    )


if __name__ == "__main__":
    parser = get_pipeline_parser()
    args = parser.parse_args()
    main(args)