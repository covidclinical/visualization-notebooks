from os.path import join

# File paths
DATA_DIR = join("..", "fakedata") # TODO: change this to `data` once real data exists

# Standard column names
class COLUMNS:
    PATIENT_ID = "patient_id"
    TIMESTAMP = "timestamp"
    EVENT = "event"
    VALUE = "value"