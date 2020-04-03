from os.path import join, isfile
from os import listdir

# File paths
# DATA_DIR = join("..", "fakedata") # Use this line to test with fake datasets
DATA_DIR = join("..", "data")

LOOKUP_DATA_DIR = join("..", "lookup_tables")

SITE_DATA_DIR = join(DATA_DIR, "site_level_data")
SITE_DATA_GLOB = join(SITE_DATA_DIR, "*", "*.csv")
SITE_FILE_REGEX = r"(.*)(?P<year>[\d]{{4}})-(?P<month>[\d]{{2}})-(?P<day>[\d]{{2}})_{file_type}-(?P<site_id>[\w]*).csv$"

COMBINED_DATA_DIR = join(DATA_DIR, "combined")
COMBINED_DATA_GLOB = join(COMBINED_DATA_DIR, "*.csv")
COMBINED_DATA_REGEX = r"(.*){file_type}-Combined(?P<year>[\d]{{2}})(?P<month>[\d]{{2}})(?P<day>[\d]{{2}}).csv$"

# Standard column names
class COLUMNS:
    """
    Site-level
    """
    SITE_ID = "siteid"
    DATE = "date"
    LOINC = "loinc"
    DAYS_SINCE_POSITIVE = "days_since_positive"
    NUM_PATIENTS = "num_patients"
    MEAN_VALUE = "mean_value"
    STDEV_VALUE = "stdev_value"
    STDEV_VAL = "stdev_val"
    ICD_CODE = "icd_code"
    ICD_VERSION = "icd_version"
    NEW_POSITIVE_CASES = "new_positive_cases"
    PATIENTS_IN_ICU = "patients_in_icu"
    NEW_DEATHS = "new_deaths"
    SEX = "sex"
    TOTAL_PATIENTS = "total_patients"
    AGE_GROUP = "age_group"
    AGE_0TO2 = "age_0to2"
    AGE_3TO5 = "age_3to5"
    AGE_6TO11 = "age_6to11"
    AGE_12TO17 = "age_12to17"
    AGE_18TO25 = "age_18to25"
    AGE_26TO49 = "age_26to49"
    AGE_50TO69 = "age_50to69"
    AGE_70TO79 = "age_70to79"
    AGE_80PLUS = "age_80plus"

    """
    Combined site-level
    """
    # DailyCounts
    UNMASKED_SITES_NEW_POSITIVE_CASES = "unmasked_sites_new_positive_cases"
    UNMASKED_SITES_PATIENTS_IN_ICU = "unmasked_sites_patients_in_icu"
    UNMASKED_SITES_NEW_DEATHS = "unmasked_sites_new_deaths"
    MASKED_SITES_NEW_POSITIVE_CASES = "masked_sites_new_positive_cases"
    MASKED_SITES_PATIENTS_IN_ICU = "masked_sites_patients_in_icu"
    MASKED_SITES_NEW_DEATHS = "masked_sites_new_deaths"
    MASKED_UPPER_BOUND_NEW_POSITIVE_CASES = "masked_upper_bound_new_positive_cases"
    MASKED_UPPER_BOUND_PATIENTS_IN_ICU = "masked_upper_bound_patients_in_icu"
    MASKED_UPPER_BOUND_NEW_DEATHS = "masked_upper_bound_new_deaths"

    # Demographics
    UNMASKED_SITES_TOTAL_PATIENTS = "unmasked_sites_total_patients"
    UNMASKED_SITES_AGE_0TO2 = "unmasked_sites_age_0to2"
    UNMASKED_SITES_AGE_3TO5 = "unmasked_sites_age_3to5"
    UNMASKED_SITES_AGE_6TO11 = "unmasked_sites_age_6to11"
    UNMASKED_SITES_AGE_12TO17 = "unmasked_sites_age_12to17"
    UNMASKED_SITES_AGE_18TO25 = "unmasked_sites_age_18to25"
    UNMASKED_SITES_AGE_26TO49 = "unmasked_sites_age_26to49"
    UNMASKED_SITES_AGE_50TO69 = "unmasked_sites_age_50to69"
    UNMASKED_SITES_AGE_70TO79 = "unmasked_sites_age_70to79"
    UNMASKED_SITES_AGE_80PLUS = "unmasked_sites_age_80plus"
    MASKED_SITES_TOTAL_PATIENTS = "masked_sites_total_patients"
    MASKED_SITES_AGE_0TO2 = "masked_sites_age_0to2"
    MASKED_SITES_AGE_3TO5 = "masked_sites_age_3to5"
    MASKED_SITES_AGE_6TO11 = "masked_sites_age_6to11"
    MASKED_SITES_AGE_12TO17 = "masked_sites_age_12to17"
    MASKED_SITES_AGE_18TO25 = "masked_sites_age_18to25"
    MASKED_SITES_AGE_26TO49 = "masked_sites_age_26to49"
    MASKED_SITES_AGE_50TO69 = "masked_sites_age_50to69"
    MASKED_SITES_AGE_70TO79 = "masked_sites_age_70to79"
    MASKED_SITES_AGE_80PLUS = "masked_sites_age_80plus"
    MASKED_UPPER_BOUND_TOTAL_PATIENTS = "masked_upper_bound_total_patients"
    MASKED_UPPER_BOUND_AGE_0TO2 = "masked_upper_bound_age_0to2"
    MASKED_UPPER_BOUND_AGE_3TO5 = "masked_upper_bound_age_3to5"
    MASKED_UPPER_BOUND_AGE_6TO11 = "masked_upper_bound_age_6to11"
    MASKED_UPPER_BOUND_AGE_12TO17 = "masked_upper_bound_age_12to17"
    MASKED_UPPER_BOUND_AGE_18TO25 = "masked_upper_bound_age_18to25"
    MASKED_UPPER_BOUND_AGE_26TO49 = "masked_upper_bound_age_26to49"
    MASKED_UPPER_BOUND_AGE_50TO69 = "masked_upper_bound_age_50to69"
    MASKED_UPPER_BOUND_AGE_70TO79 = "masked_upper_bound_age_70to79"
    MASKED_UPPER_BOUND_AGE_80PLUS = "masked_upper_bound_age_80plus"

    # Diagnoses
    UNMASKED_SITES_NUM_PATIENTS = "unmasked_sites_num_patients"
    MASKED_SITES_NUM_PATIENTS = "masked_sites_num_patients"
    MASKED_UPPER_BOUND_NUM_PATIENTS = "masked_upper_bound_num_patients"

    # Labs
    UNMASKED_SITES_NUM_PATIENTS = "unmasked_sites_num_patients"
    MASKED_SITES_NUM_PATIENTS = "masked_sites_num_patients"
    MASKED_UPPER_BOUND_NUM_PATIENTS = "masked_upper_bound_num_patients"

    """
    Patient-level
    """
    PATIENT_ID = "patient_id"
    TIMESTAMP = "timestamp"
    EVENT = "event"
    VALUE = "value"

ALL_AGE_COLUMNS = [
    COLUMNS.AGE_0TO2,
    COLUMNS.AGE_3TO5,
    COLUMNS.AGE_6TO11,
    COLUMNS.AGE_12TO17,
    COLUMNS.AGE_18TO25,
    COLUMNS.AGE_26TO49,
    COLUMNS.AGE_50TO69,
    COLUMNS.AGE_70TO79,
    COLUMNS.AGE_80PLUS
]

class SITE_FILE_TYPES:
    DAILY_COUNTS = "DailyCounts"
    DEMOGRAPHICS = "Demographics"
    DIAGNOSES = "Diagnoses"
    LABS = "Labs"

ALL_SITE_FILE_TYPES = [
    SITE_FILE_TYPES.DAILY_COUNTS,
    SITE_FILE_TYPES.DEMOGRAPHICS,
    SITE_FILE_TYPES.DIAGNOSES,
    SITE_FILE_TYPES.LABS
]