from os.path import join, isfile
from os import listdir

# File paths
DATA_DIR = join("..", "fakedata") # TODO: change this to `data` once real data exists

SITE_DATA_DIR = join(DATA_DIR, "site_level_data")
SITE_DATA_GLOB = join(SITE_DATA_DIR, "*", "*.csv")
SITE_FILE_REGEX = r"(.*)(?P<year>[\d]{{4}})-(?P<month>[\d]{{2}})-(?P<day>[\d]{{2}})_{file_type}-(?P<site_id>[\w]*).csv$"

# Standard column names
class COLUMNS:
    # Site-level
    SITE_ID = "siteid"
    DATE = "date"
    LOINC = "loinc"
    DAYS_SINCE_POSITIVE = "days_since_positive"
    NUM_PATIENTS = "num_patients"
    MEAN_VALUE = "mean_value"
    STDEV_VALUE = "stdev_value"
    ICD_CODE = "icd_code"
    ICD_VERSION = "icd_version"
    NEW_POSITIVE_CASES = "new_positive_cases"
    PATIENTS_IN_ICU = "patients_in_icu"
    NEW_DEATHS = "new_deaths"
    SEX = "sex"
    TOTAL_PATIENTS = "total_patients"
    AGE_0TO2 = "age_0to2"
    AGE_3TO5 = "age_3to5"
    AGE_6TO11 = "age_6to11"
    AGE_12TO17 = "age_12to17"
    AGE_18TO25 = "age_18to25"
    AGE_26TO49 = "age_26to49"
    AGE_50TO69 = "age_50to69"
    AGE_70TO79 = "age_70to79"
    AGE_80PLUS = "age_80plus"

    # Patient-level
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