
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta

from constants import COLUMNS
from utils import read_latest_daily_counts_df

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

    ################# Debug
    # df = read_latest_daily_counts_df()
    # qfield = "new_positive_cases"
    # datefield = "date"
    # gte = 10
    ######################

    timestep = "timestep"
    df_copy = df.copy()
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
        
        for idx in df_by_site.index:
            ref_date_obj = datetime.strptime(reference_date, '%Y-%m-%d')
            cur_date_obj = datetime.strptime(df_copy[datefield][idx], '%Y-%m-%d')

            df_copy[timestep][idx] = (cur_date_obj - ref_date_obj).days

    return df_copy