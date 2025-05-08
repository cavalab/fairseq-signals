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
    # TODO - Use `row["path"]` to load the sample

    print(vars(row))
    for k, v in row.items():
        print(k, ":", v)
    ecg_file = row["path"]
    ecg_file = h5py.File(os.path.join(args.raw_root, ecg_file), "r")

    fields = {
        "sample_rate": 500  # TODO - Extract sample rate from the row or the file
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
    data = {
        "org_sample_rate": fields["sample_rate"],
        "curr_sample_rate": fields["sample_rate"],
        "org_sample_size": feats.shape[1],
        "curr_sample_size": feats.shape[1],
        "feats": feats,
        "idx": row["idx"],
    }
    savemat(row["save_path"], data)

    fields["avail_leads"] = str(avail_leads)

    # Recommended to extract feature information on mean, STD, nulls, and constants
    fields.update(extract_feat_info(feats, leads_to_load))

    # Return the extracted metadata
    meta = pd.Series(fields)

    return meta

    # Optionally, multiple DataFrame objects can be returned in a dictionary format,
    # which is useful for extracting data with multiple entries per sample - if done
    # this way, there must be a 'meta' entry
    qrs_times = ...

    return {"meta": meta, "qrs_times": qrs_times}


def postprocess_meta(meta):
    """
    Perform operations on the combined meta extracted using the `extract_func`.

    This may include dropping or renaming columns, mapping values, or performing
    other such transformations.
    """
    # TODO - Optional (can remove `postprocess_extraction` argument if unneeded)

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
        extract_func=extract_bch,
        # postprocess_extraction={'meta': postprocess_meta},
    )


if __name__ == "__main__":
    parser = get_pipeline_parser()
    args = parser.parse_args()
    main(args)

# def main(args):
#     global HDF

#     try:
#         records = pd.read_csv(os.path.join(args.processed_root, "records.csv"))
#     except FileNotFoundError as err:
#         raise FileNotFoundError(
#             'Run bch_records.py first.'
#         ) from err

#     # records['path'] = records['exam_id'] # Need this to pass column checking
#     records['save_file'] = 'bch_' + records['exam_id'].astype(str) + '.mat'
#     records["source"] = SOURCE
#     records["dataset"] = SOURCE

#     # there is one ECG file
#     ecg_file = records['path'].values[0]
#     HDF = h5py.File(os.path.join(args.raw_root, ecg_file), 'r')

#     # Note: last sample has non-existent exam_id 0 and has all-zero tracing
#     exam_ids = {key: np.array(HDFs[key]['exam_id'][:])[:-1] for key in HDFs}

#     exam_id_to_ind = {}
#     for key in HDFs:
#         exam_id_to_ind.update(dict(zip(exam_ids[key], np.arange(len(exam_ids[key])))))

#     records['hdf_ind'] = records['exam_id'].map(exam_id_to_ind)

#     pipeline(
#         args,
#         records,
#         SOURCE,
#         extract_func=extract_bch,
#     )

# if __name__ == "__main__":
#     parser = get_pipeline_parser()
#     args = parser.parse_args()
#     main(args)
