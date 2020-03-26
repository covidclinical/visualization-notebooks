from os.path import join
from enum import Enum

# File paths
DATA_DIR = join("..", "data")

# Standard column names
class TIMELINE_COLUMNS(Enum):
    PATIENT_ID = "patient_id"
    TIMESTAMP = "timestamp"
    VALUE = "value"