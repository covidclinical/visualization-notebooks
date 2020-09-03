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
    ALL_SITE_FILE_TYPES,
    SINGLE_SITE_COUNTRIES,
    MERGED_SINGLE_SITE_COUNTRIES_NAME
)

"""
Constants and utilities for merging countries
"""

def merge_single_site_country_name(country_name):
    if country_name in SINGLE_SITE_COUNTRIES:
        return MERGED_SINGLE_SITE_COUNTRIES_NAME
    return country_name

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
        # Column names have white spaces and double quotation marks which shouldn't be
        df = df.rename(columns=dict(zip(columns, [ col.lower().replace(' ', '').replace('"', '') for col in columns ])))
        site_dfs.append(df)

    full_df = pd.concat(site_dfs, ignore_index=True)
    # Convert site IDs to uppercase to remove any discrepancies between the ID in the SiteID_Map.csv and the data folder/filenames.
    full_df["siteid"] = full_df["siteid"].apply(lambda x: x.upper())

    # Remove a fake site
    full_df = full_df[full_df['siteid'] != 'FICHOS']

    # Remove sites that are not included in our mapping table
    full_df = full_df[full_df['siteid'].isin(get_siteid_country_map().keys())]

    # Add Country name and color
    siteid_to_country = get_siteid_country_map()
    siteid_to_color = get_siteid_color_maps()
    siteid_to_pediatric = get_siteid_pediatric_maps()
    full_df['country'] = full_df['siteid'].apply(lambda x: siteid_to_country[x])
    full_df['color'] = full_df['siteid'].apply(lambda x: siteid_to_color[x])
    full_df['pediatric'] = full_df['siteid'].apply(lambda x: siteid_to_pediatric[x])
    return full_df

def read_full_demographics_df():
    df = read_full_site_df(get_site_file_info(), SITE_FILE_TYPES.DEMOGRAPHICS)
    df["sex"] = df["sex"].apply(lambda x: x.strip() if type(x) == str else x)
    df["race"] = df["race"].apply(lambda x: x.strip() if type(x) == str else x)
    df["age_group"] = df["age_group"].apply(lambda x: x.strip() if type(x) == str else x)
    df["num_patients_all"] = df["num_patients_all"].astype(int)
    df["num_patients_ever_severe"] = df["num_patients_ever_severe"].astype(int)
    return df

def read_full_lab_df():
    df = read_full_site_df(get_site_file_info(), SITE_FILE_TYPES.LABS)
    df["days_since_admission"] = df["days_since_admission"].astype(int)
    df["num_patients_all"] = df["num_patients_all"].astype(int)
    df["mean_value_all"] = df["mean_value_all"].astype(float)
    df["stdev_value_all"] = df["stdev_value_all"].astype(float)
    df["mean_log_value_all"] = df["mean_log_value_all"].astype(float)
    df["stdev_log_value_all"] = df["stdev_log_value_all"].astype(float)
    df["num_patients_ever_severe"] = df["num_patients_ever_severe"].astype(int)
    df["mean_value_ever_severe"] = df["mean_value_ever_severe"].astype(float)
    df["stdev_value_ever_severe"] = df["stdev_value_ever_severe"].astype(float)
    df["mean_log_value_ever_severe"] = df["mean_log_value_ever_severe"].astype(float)
    df["stdev_log_value_ever_severe"] = df["stdev_log_value_ever_severe"].astype(float)
    return df

def read_full_med_df():
    df = read_full_site_df(get_site_file_info(), SITE_FILE_TYPES.MEDICATIONS)
    df["num_patients_all_before_admission"] = df["num_patients_all_before_admission"].astype(int)
    df["num_patients_all_since_admission"] = df["num_patients_all_since_admission"].astype(int)
    df["num_patients_ever_severe_before_admission"] = df["num_patients_ever_severe_before_admission"].astype(int)
    df["num_patients_ever_severe_since_admission"] = df["num_patients_ever_severe_since_admission"].astype(int)
    return df

def read_full_cli_df():
    df = read_full_site_df(get_site_file_info(), SITE_FILE_TYPES.CLINICAL_COURSE)
    df["days_since_admission"] = df["days_since_admission"].astype(int)
    df["num_patients_all_still_in_hospital"] = df["num_patients_all_still_in_hospital"].astype(int)
    df["num_patients_ever_severe_still_in_hospital"] = df["num_patients_ever_severe_still_in_hospital"].astype(int)
    return df

def read_full_daily_counts_df():
    df = read_full_site_df(get_site_file_info(), SITE_FILE_TYPES.DAILY_COUNTS)
    df["cumulative_patients_all"] = df["cumulative_patients_all"].astype(int)
    df["cumulative_patients_severe"] = df["cumulative_patients_severe"].astype(int)
    df["cumulative_patients_dead"] = df["cumulative_patients_dead"].astype(int)
    df["num_patients_in_hospital_on_this_date"] = df["num_patients_in_hospital_on_this_date"].astype(int)
    df["num_patients_in_hospital_and_severe_on_this_date"] = df["num_patients_in_hospital_and_severe_on_this_date"].astype(int)
    df["calendar_date"] = df["calendar_date"].astype(str)
    def convert_date(date_str):
        try:
            return dateutil.parser.parse(date_str)
        except:
            return np.nan
    df["calendar_date"] = df["calendar_date"].apply(convert_date)
    return df

"""
Helpers for reading additional data files.
"""
def read_loinc_df():
    return pd.read_csv(join(LOOKUP_DATA_DIR, "lab_table.txt"), sep="\t", header=0)

def read_site_details_df():
    # No detail information for each site yet
    return pd.read_csv(join(DATA_DIR, "SiteID_Map.csv"), sep=",", header=0)

def get_siteid_anonymous_map():
    df = read_site_details_df().sort_values(by=["Anonymous Site ID"])
    df = df.reset_index()
    return dict(zip(df["Acronym"].values.tolist(), df["Anonymous Site ID"].values.tolist()))

# TODO: Clean codes for supporting pediatric and none pediatric sites.
def read_none_pediatric_site_details_df():
    # No detail information for each site yet
    return pd.read_csv(join(DATA_DIR, "SiteID_Map_None_Pediatric.csv"), sep=",", header=0)

def read_pediatric_site_details_df():
    # No detail information for each site yet
    return pd.read_csv(join(DATA_DIR, "SiteID_Map_Pediatric.csv"), sep=",", header=0)

def get_siteid_anonymous_map():
    df = read_site_details_df().sort_values(by=["Anonymous Site ID"])
    df = df.reset_index()
    return dict(zip(df["Acronym"].values.tolist(), df["Anonymous Site ID"].values.tolist()))

def get_siteid_country_map():
    df = read_site_details_df()
    df = df.reset_index()
    return dict(zip(df["Acronym"].values.tolist(), df["Country"].values.tolist()))

def get_siteid_color_maps():
    df = read_site_details_df()
    df = df.reset_index()
    site_country_map = dict(zip(df["Acronym"].values.tolist(), df["Country Color"].values.tolist()))
    return site_country_map

def get_siteid_pediatric_maps():
    df = read_site_details_df()
    df = df.reset_index()
    return dict(zip(df["Acronym"].values.tolist(), df["Pediatric"].values.tolist()))

def get_siteid_color_maps_none_pediatric():
    df = read_none_pediatric_site_details_df()
    df = df.reset_index()
    site_country_map = dict(zip(df["Acronym"].values.tolist(), df["Country Color"].values.tolist()))
    return site_country_map

def get_siteid_color_maps_pediatric():
    df = read_pediatric_site_details_df()
    df = df.reset_index()
    site_country_map = dict(zip(df["Acronym"].values.tolist(), df["Country Color"].values.tolist()))
    return site_country_map

def get_anonymousid_color_maps():
    df = read_site_details_df().sort_values(by=["Anonymous Site ID"])
    df = df.reset_index()
    anonymousid_country_map = dict(zip(df["Anonymous Site ID"].values.tolist(), df["Country Color"].values.tolist()))
    return anonymousid_country_map

def get_anonymousid_color_maps_pediatric():
    df = read_pediatric_site_details_df().sort_values(by=["Anonymous Site ID"])
    df = df.reset_index()
    anonymousid_country_map = dict(zip(df["Anonymous Site ID"].values.tolist(), df["Country Color"].values.tolist()))
    return anonymousid_country_map

def get_anonymousid_color_maps_none_pediatric():
    df = read_none_pediatric_site_details_df().sort_values(by=["Anonymous Site ID"])
    df = df.reset_index()
    anonymousid_country_map = dict(zip(df["Anonymous Site ID"].values.tolist(), df["Country Color"].values.tolist()))
    return anonymousid_country_map

def get_country_color_map_pediatric():
    df = read_pediatric_site_details_df()
    df = df.reset_index()
    df = df.drop_duplicates(subset=["Country"])
    return dict(zip(df["Country"].values.tolist(), df["Country Color"].values.tolist()))

def get_country_color_map_none_pediatric():
    df = read_none_pediatric_site_details_df()
    df = df.reset_index()
    df = df.drop_duplicates(subset=["Country"])
    return dict(zip(df["Country"].values.tolist(), df["Country Color"].values.tolist()))

def get_country_color_map(merge_single_site_countries=False):
    df = read_site_details_df()
    df = df.reset_index()
    df = df.drop_duplicates(subset=["Country"])
    result = dict(zip(df["Country"].values.tolist(), df["Country Color"].values.tolist()))
    if merge_single_site_countries:
        for country_name in SINGLE_SITE_COUNTRIES:
            del result[country_name]
        result[MERGED_SINGLE_SITE_COUNTRIES_NAME] = "#56B4E9"
    return result

"""
Helpers to apply high-level themes to altair charts.
"""
def apply_theme(
    base,
    title_anchor="middle",
    title_font_size=18,
    axis_title_font_size=16,
    axis_label_font_size=14,
    axis_title_padding=10,
    label_angle=0,
    legend_orient="right",
    legend_title_orient="top",
    legend_stroke_color="lightgray",
    legend_padding=10,
    legend_symbol_type="circle",
    legend_title_font_size=16,
    label_font_size=14,
    header_label_font_size=13
):
    return base.configure_view(
        # ...
    ).configure_header(
        titleFontSize=16,
        titleFontWeight=300,
        labelFontSize=header_label_font_size
    ).configure_title(
        fontSize=title_font_size,
        fontWeight=400,
        anchor=title_anchor,
        align="left"
    ).configure_axis(
        labelFontSize=axis_label_font_size,
        labelFontWeight=300,
        titleFontSize=axis_title_font_size,
        titleFontWeight=300,
        labelLimit=1000,
        titlePadding=axis_title_padding
        # labelAngle=label_angle
    ).configure_legend(
        titleFontSize=legend_title_font_size,
        titleFontWeight=400,
        labelFontSize=label_font_size,
        labelFontWeight=300,
        padding=legend_padding,
        cornerRadius=0,
        orient=legend_orient,
        fillColor="white",
        strokeColor=legend_stroke_color,
        symbolType=legend_symbol_type,
        titleOrient=legend_title_orient
    ).configure_concat(
        spacing=0
    )

def get_visualization_subtitle(data_release='YYYY-MM-DD', with_num_sites=True, num_sites=None, cohort=None):
    parts = [f"Data as of {data_release}"]
    
    if with_num_sites:
        if num_sites == None:
            num_sites = len(read_full_lab_df()['siteid'].unique())
        parts += [f"{num_sites} Sites"]
    
    if cohort != None:
        parts += [cohort]
    
    return " | ".join(parts)