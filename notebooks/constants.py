from os.path import join, isfile
from os import listdir

# File paths
DATA_DIR = join("..", "fakedata") # TODO: change this to `data` once real data exists

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

# List of all site IDs for which there is data in `DATA_DIR`
SITE_IDS = [
    "FMC", # fake medical center
    "FCH", # fake children's hospital
]

# We can use the following 20 site IDs when generating fake datasets
# ['FWN','FXL','FZT','FMT','FFG','FOW','FSZ','FMA','FEQ','FVX','FKQ','FBL','FDQ','FKN','FBD','FKL','FUU','FZU','FZM','FUN']

# Collect all site IDs by looking into file names in `DATA_DIR`.
filenames = [f for f in listdir(DATA_DIR) if isfile(join(DATA_DIR, f))]
    
_SITE_IDS_FOR_DAILY_COUNT_FILES = [fname[len("DailyCounts-"):-len(".csv")] for fname in filenames if "DailyCounts-" in fname]
_SITE_IDS_FOR_DEMOGRAPHICS_FILES = [fname[len("Demographics-"):-len(".csv")] for fname in filenames if "Demographics-" in fname]
_SITE_IDS_FOR_LABS_FILES = [fname[len("Labs-"):-len(".csv")] for fname in filenames if "Labs-" in fname]
_SITE_IDS_FOR_DIAGNOSES_FILES = [fname[len("Diagnoses-"):-len(".csv")] for fname in filenames if "Diagnoses-" in fname]

# List of all site IDs collected by looking into the file names in `DATA_DIR`.
class SITE_IDS_IN_DIR:
    DAILY_COUNT = _SITE_IDS_FOR_DAILY_COUNT_FILES
    DEMOGRAPHICS = _SITE_IDS_FOR_DEMOGRAPHICS_FILES
    LABS = _SITE_IDS_FOR_LABS_FILES
    DIAGNOSES = _SITE_IDS_FOR_DIAGNOSES_FILES
    INTERSECTION = list(
        set(_SITE_IDS_FOR_DAILY_COUNT_FILES) & 
        set(_SITE_IDS_FOR_DEMOGRAPHICS_FILES) & 
        set(_SITE_IDS_FOR_LABS_FILES) &
        set(_SITE_IDS_FOR_DIAGNOSES_FILES)
    )
    UNION = list(
        set(_SITE_IDS_FOR_DAILY_COUNT_FILES) | 
        set(_SITE_IDS_FOR_DEMOGRAPHICS_FILES) | 
        set(_SITE_IDS_FOR_LABS_FILES) |
        set(_SITE_IDS_FOR_DIAGNOSES_FILES)
    )