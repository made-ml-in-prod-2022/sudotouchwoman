from os.path import isfile

TMP_DIR_NAME = "tmp/"
SAMPLE_PICKLE_PATH = "data/artifact.pkl"
SAMPLE_PREDICTION_REQUEST = "data/payload.json"

artifact_present = isfile(SAMPLE_PICKLE_PATH)
