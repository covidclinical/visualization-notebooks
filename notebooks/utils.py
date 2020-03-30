import re
import glob
import datetime
import pandas as pd
import numpy as np
from os.path import join

from constants import (
    COLUMNS,
    SITE_DATA_GLOB, 
    SITE_FILE_REGEX, 
    SITE_FILE_TYPES, 
    ALL_SITE_FILE_TYPES
)

"""
Utilities for listing site file information.
"""
def get_site_file_paths():
    return glob.glob(SITE_DATA_GLOB)

def get_site_file_info(file_types=ALL_SITE_FILE_TYPES):
    file_paths = get_site_file_paths()
    potential_matches = [ 
        (re.match(SITE_FILE_REGEX.format(file_type=ft), fp), ft)
            for ft in file_types 
            for fp in file_paths 
    ]
    all_info = [ dict(**m.groupdict(), file_type=ft, file_path=m[0]) for m, ft in potential_matches if m is not None ]
    for info in all_info:
        info["date"] = datetime.date(int(info["year"]), int(info["month"]), int(info["day"]))
    return all_info

def get_site_ids(file_types=ALL_SITE_FILE_TYPES):
    all_site_file_info = get_site_file_info(file_types=file_types)
    return list(set([ info["site_id"] for info in all_site_file_info ]))

def get_latest_site_file_info(file_types=ALL_SITE_FILE_TYPES):
    # For each site ID, only get the latest info dict for each site file type
    all_site_file_info = get_site_file_info(file_types=file_types)
    sorted_site_file_info = sorted(all_site_file_info, key=lambda info: (info["site_id"], info["file_type"], info["date"]), reverse=True)
    unique_site_file_info = dict()
    for info in sorted_site_file_info:
        key = (info["site_id"], info["file_type"])
        if key not in unique_site_file_info:
            unique_site_file_info[key] = info
    return list(unique_site_file_info.values())

def get_site_file_info_by_date(year, month, day, file_types=ALL_SITE_FILE_TYPES):
    target_date = datetime.date(year, month, day)
    all_site_file_info = get_site_file_info(file_types=file_types)
    return [ info for info in all_site_file_info if info["date"] == target_date ]


"""
Utilities for reading in data from a list of site info for each file type.
"""

def read_full_site_df(site_file_info, file_type, columns):
    filtered_site_file_info = [ info for info in site_file_info if info["file_type"] == file_type ]

    site_dfs = []
    for info in filtered_site_file_info:
        df = pd.read_csv(info["file_path"], header=None)
        #df[COLUMNS.SITE_ID] = info["site_id"]
        site_dfs.append(df)

    full_df = pd.concat(site_dfs, ignore_index=True)
    full_df = full_df.rename(columns=dict(zip(range(len(columns)), columns)))
    return full_df

def read_full_daily_counts_df(site_file_info):
    return read_full_site_df(site_file_info, SITE_FILE_TYPES.DAILY_COUNTS, [
        COLUMNS.SITE_ID,
        COLUMNS.DATE,
        COLUMNS.NEW_POSITIVE_CASES,
        COLUMNS.PATIENTS_IN_ICU,
        COLUMNS.NEW_DEATHS
    ])

def read_full_demographics_df(site_file_info):
    return read_full_site_df(site_file_info, SITE_FILE_TYPES.DEMOGRAPHICS, [
        COLUMNS.SITE_ID,
        COLUMNS.SEX,
        COLUMNS.TOTAL_PATIENTS,
        COLUMNS.AGE_0TO2,
        COLUMNS.AGE_3TO5,
        AGE_6TO11,
        AGE_12TO17,
        AGE_18TO25,
        AGE_26TO49,
        AGE_50TO69,
        AGE_70TO79,
        AGE_80PLUS
    ])

def read_full_diagnoses_df(site_file_info):
    return read_full_site_df(site_file_info, SITE_FILE_TYPES.DIAGNOSES, [
        COLUMNS.SITE_ID,
        COLUMNS.ICD_CODE,
        COLUMNS.ICD_VERSION,
        COLUMNS.NUM_PATIENTS
    ])

def read_full_labs_df(site_file_info):
    return read_full_site_df(site_file_info, SITE_FILE_TYPES.LABS, [
        COLUMNS.SITE_ID,
        COLUMNS.LOINC,
        COLUMNS.DAYS_SINCE_POSITIVE,
        COLUMNS.NUM_PATIENTS,
        COLUMNS.MEAN_VALUE,
        COLUMNS.STDEV_VALUE
    ])

"""
Helpers for reading all of the latest data for each site file type.
"""

def read_latest_daily_counts_df():
    return read_full_daily_counts_df(get_latest_site_file_info())

def read_latest_demographics_df():
    return read_full_demographics_df(get_latest_site_file_info())

def read_latest_diagnoses_df():
    return read_full_diagnoses_df(get_latest_site_file_info())

def read_latest_labs_df():
    return read_full_labs_df(get_latest_site_file_info())

"""
Helpers for reading additional data files.
"""
def read_icd_df():
    return pd.read_csv(join(DATA_DIR, "icdMappingFile.txt"), sep="\t", header=0)
