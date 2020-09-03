from os.path import join, isfile
from os import listdir

# File paths
# DATA_DIR = join("..", "fakedata") # Use this line to test with fake datasets
DATA_DIR = join("..", "data")

LOOKUP_DATA_DIR = "lookup_tables"
SITE_DATA_DIR = join(DATA_DIR, "Phase1.1")

SITE_PATH_GLOB = join(SITE_DATA_DIR, "latest", "*.csv")
SITE_FILE_REGEX = r"(.*){file_type}-(?P<site_id>[\w]*).csv$"

class SITE_FILE_TYPES:
    CLINICAL_COURSE = "ClinicalCourse"
    DAILY_COUNTS = "DailyCounts"
    DEMOGRAPHICS = "Demographics"
    DIAGNOSES = "Diagnoses"
    LABS = "Labs"
    MEDICATIONS = "Medications"

ALL_SITE_FILE_TYPES = [
    SITE_FILE_TYPES.CLINICAL_COURSE,
    SITE_FILE_TYPES.DAILY_COUNTS,
    SITE_FILE_TYPES.DEMOGRAPHICS,
    SITE_FILE_TYPES.DIAGNOSES,
    SITE_FILE_TYPES.LABS,
    SITE_FILE_TYPES.MEDICATIONS
]

SINGLE_SITE_COUNTRIES = ["Germany", "Singapore", "UK"]
MERGED_SINGLE_SITE_COUNTRIES_NAME = " + ".join(SINGLE_SITE_COUNTRIES)