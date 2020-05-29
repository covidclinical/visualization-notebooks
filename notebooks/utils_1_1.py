import re
import glob
import pandas as pd
import numpy as np
import datetime
import dateutil.parser
from os.path import join


from constants_1_1 import (
    DATA_DIR,
    LOOKUP_DATA_DIR,
    SITE_DATA_DIR,
    SITE_PATH_GLOB,
    SITE_FILE_REGEX,
    SITE_FILE_TYPES,
    ALL_SITE_FILE_TYPES
)

"""
Utilities for listing site file information.
"""
def get_site_file_paths():
    return glob.glob(SITE_PATH_GLOB)

def get_site_file_info(file_types=ALL_SITE_FILE_TYPES):
    file_paths = get_site_file_paths()
    potential_matches = [
        (re.match(SITE_FILE_REGEX.format(file_type=ft), fp), ft)
            for ft in file_types
            for fp in file_paths
    ]
    all_info = [ dict(**m.groupdict(), file_type=ft, file_path=m[0]) for m, ft in potential_matches if m is not None ]
    return all_info

def get_site_ids(file_types=ALL_SITE_FILE_TYPES):
    all_site_file_info = get_site_file_info(file_types=file_types)
    return list(set([ info["site_id"] for info in all_site_file_info ]))


"""
Utilities for reading in data from a list of site info for each file type.
"""
def read_full_site_df(site_file_info, file_type):
    filtered_site_file_info = [ info for info in site_file_info if info["file_type"] == file_type ]

    site_dfs = []
    for info in filtered_site_file_info:
        df = pd.read_csv(info["file_path"])
        columns = df.columns.values.tolist()
        # Case of column names is inconsistent
        df = df.rename(columns=dict(zip(columns, [ col.lower() for col in columns ])))

        site_dfs.append(df)

    full_df = pd.concat(site_dfs, ignore_index=True)
    return full_df

def read_full_demographics_df():
    df = read_full_site_df(get_site_file_info(), SITE_FILE_TYPES.DEMOGRAPHICS)
    df["num_patients_all"] = df["num_patients_all"].astype(int)
    df["num_patients_ever_severe"] = df["num_patients_ever_severe"].astype(int)
    return df
