import re
import glob
import pandas as pd
import numpy as np
import datetime
from os.path import join


from constants import (
    COLUMNS,
    DATA_DIR,
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
        if df.shape[0] > 0 and df.iloc[0,0].lower() in [ "site_id", "siteid" ]:
            # This file has a header but should not have one.
            df = df.drop(index=[0])
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
        COLUMNS.AGE_6TO11,
        COLUMNS.AGE_12TO17,
        COLUMNS.AGE_18TO25,
        COLUMNS.AGE_26TO49,
        COLUMNS.AGE_50TO69,
        COLUMNS.AGE_70TO79,
        COLUMNS.AGE_80PLUS
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
Helpers for cleaning datasets after reading them to visualize.
"""
def clean_demographics_df(df):
    # Use more readable column names
    df = df.rename(columns={
        "age_0to2": "0-2",
        "age_3to5": "3-5",
        "age_6to11": "6-11",
        "age_12to17": "12-17",
        "age_18to25": "18-25",
        "age_26to49": "26-49",
        "age_50to69": "50-69",
        "age_70to79": "70-79",
        "age_80plus": "80+"
    })
    # Use the consistent capitalization
    df[COLUMNS.SEX] = df[COLUMNS.SEX].apply(lambda x: x.capitalize())
    return df

def clean_daily_counts_df(df):
    # Change variables to more readable names
    df = df.rename(columns={
        "new_positive_cases": "New positive cases",
        "new_deaths": "New deaths",
        "patients_in_icu": "Patients in ICU"
    })
    return df

"""
Helpers for reading additional data files.
"""
def read_icd_df():
    return pd.read_csv(join(DATA_DIR, "mappingICD_CCS.txt"), sep="\t", header=0)

def read_loinc_df():
    return pd.read_csv(join(DATA_DIR, "labMap.csv"), header=0)

"""
Utilities to manipulating data.
"""
def add_aligned_time_steps_column(df, qfield, datefield, gte):
    """
    This function adds a new column, called `timestep`, that represent the number of time steps
    after the cumulative value of `qfield` becomes equal or larger than `gte` value. `0` represents
    a time point when the value meats the `gte` condition, `1` represents the next day, and so on.

    df: Pandas DataFrame to manipulate data
    qfield: A field that contains quantitative values
    datefield: A field that contains date in a "YYYY-MM-DD" format.
    gte: The value to compare
    """

    ######## Debug #######
    # df = read_latest_daily_counts_df()
    # qfield = "new_positive_cases"
    # datefield = "date"
    # gte = 10
    ######################

    timestep = "timestep"
    df_copy = df.copy(deep=True)
    df_copy[timestep] = -1

    SITE_IDS = df[COLUMNS.SITE_ID].unique().tolist()

    for siteid in SITE_IDS:
        # Get only the rows for this siteid & sort them by date
        df_by_site = df_copy[df_copy["siteid"] == siteid]
        df_by_site = df_by_site.sort_values(by=datefield, ascending=True)

        cumulative_value = 0
        reference_date = ""
        for idx in df_by_site.index:
            cumulative_value += df_copy[qfield][idx]
            if cumulative_value > gte:
                reference_date = df_copy[datefield][idx]
                break

        if reference_date != "":
            for idx in df_by_site.index:
                ref_date_obj = datetime.datetime.strptime(reference_date, '%Y-%m-%d')
                cur_date_obj = datetime.datetime.strptime(df_copy[datefield][idx], '%Y-%m-%d')

                df_copy.loc[idx, 'timestep'] = (cur_date_obj - ref_date_obj).days

    return df_copy

"""
Utilities to customize visualizations.
"""
def apply_theme(base, legend_orient="top-left"):
    return base.configure_axis(
        labelFontSize=14,
        labelFontWeight=300,
        titleFontSize=18,
        titleFontWeight=300,
        labelLimit=1000,
    ).configure_title(fontSize=18, fontWeight=400, anchor="middle"
    ).configure_legend(
        titleFontSize=18, titleFontWeight=400,
        labelFontSize=16, labelFontWeight=300,
        padding=10,
        cornerRadius=0,
        orient=legend_orient,
        fillColor="white",
        strokeColor="lightgray"
    ).configure_view(
        # stroke="black",
        # strokeWidth=3
    )

def apply_trellis_theme(base):
    return base.configure_axis(
        labelFontSize=14,
        labelFontWeight=300,
        titleFontSize=18,
        titleFontWeight=400,
        labelLimit=1000,
        gridColor="#f0f0f0",
        # gridOpacity=0,
        domainOpacity=0,
        # tickOpacity=0
        tickColor="lightgray"
        # grid=False
    ).configure_title(
        fontSize=22, fontWeight=400, anchor="middle",
        dx=160, dy=-15
        # dx=382, dy=35
    ).configure_legend(
        titleFontSize=18, titleFontWeight=400,
        labelFontSize=16, labelFontWeight=300,
        padding=10,
        cornerRadius=0,
        labelLimit=1000,
        # strokeColor="lightgray"
    ).configure_view(
        stroke="lightgray",
        strokeWidth=2
        # strokeOpacity=0
    ).configure_header(
        # titleFontSize=18,
        # titleFontWeight=300,
        labelFontSize=18,
    ).configure_concat(
        spacing=-50
    ).configure_facet(
        spacing=6
    )

def apply_grouped_bar_theme(base, legend_orient="top-left", strokeColor=None):
    return base.configure_axis(
        labelFontSize=14,
        labelFontWeight=300,
        titleFontSize=18,
        titleFontWeight=300,
        labelLimit=1000,
        # grid=False
    ).configure_title(fontSize=18, fontWeight=400, anchor="middle"
    ).configure_legend(
        titleFontSize=18, titleFontWeight=400,
        labelFontSize=16, labelFontWeight=300,
        fillColor="white",
        strokeColor=strokeColor,
        padding=10,
        cornerRadius=0,
        orient=legend_orient
    ).configure_view(
        # stroke=None
        # strokeWidth=3
    ).configure_header(
        titleFontSize=16,
        titleFontWeight=300,
        labelFontSize=13
    )