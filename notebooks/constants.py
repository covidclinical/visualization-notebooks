from os.path import join

# File paths
DATA_DIR = join("..", "fakedata") # TODO: change this to `data` once real data exists

# Standard column names
class COLUMNS:
    PATIENT_ID = "patient_id"
    TIMESTAMP = "timestamp"
    EVENT = "event"
    VALUE = "value"
    SITE_ID = "siteid"
    LOINC = "loinc"
    DAYS_SINCE_POSITIVE = "days_since_positive"
    NUM_PATIENTS = "num_patients"
    MEAN_VALUE = "mean_value"
    STDEV_VALUE = "stdev_value"