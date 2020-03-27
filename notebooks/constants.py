from os.path import join

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