import pandas as pd
import numpy as np
from os.path import join

from constants import DATA_DIR, COLUMNS

"""
Utilities for reading in data from all sites for each file type.
"""

def read_full_df(prefix, site_ids):
    return pd.concat((pd.read_csv(join(DATA_DIR, f"{prefix}-{site_id}.csv"), header=None) for site_id in site_ids), ignore_index=True)

def read_full_daily_counts_df(site_ids):
    return read_full_df("DailyCounts", site_ids).rename(columns={
        0: COLUMNS.SITE_ID,
        1: COLUMNS.DATE,
        2: COLUMNS.NEW_POSITIVE_CASES,
        3: COLUMNS.PATIENTS_IN_ICU,
        4: COLUMNS.NEW_DEATHS
    })

def read_full_demographics_df(site_ids):
    return read_full_df("Demographics", site_ids).rename(columns={
        0: COLUMNS.SITE_ID,
        1: COLUMNS.SEX,
        2: COLUMNS.TOTAL_PATIENTS,
        3: COLUMNS.AGE_0TO2,
        4: COLUMNS.AGE_3TO5,
        5: AGE_6TO11,
        6: AGE_12TO17,
        7: AGE_18TO25,
        8: AGE_26TO49,
        9: AGE_50TO69,
        10: AGE_70TO79,
        11: AGE_80PLUS
    })

def read_full_diagnoses_df(site_ids):
    return read_full_df("Diagnoses", site_ids).rename(columns={
        0: COLUMNS.SITE_ID,
        1: COLUMNS.ICD_CODE,
        2: COLUMNS.ICD_VERSION,
        3: COLUMNS.NUM_PATIENTS
    })

def read_full_labs_df(site_ids):
    return read_full_df("Labs", site_ids).rename(columns={
        0: COLUMNS.SITE_ID,
        1: COLUMNS.LOINC,
        2: COLUMNS.DAYS_SINCE_POSITIVE,
        3: COLUMNS.NUM_PATIENTS,
        4: COLUMNS.MEAN_VALUE,
        5: COLUMNS.STDEV_VALUE
    })

def read_icd_df():
    return pd.read_csv(join(DATA_DIR, "icdMappingFile.txt"), sep="\t", header=0)
