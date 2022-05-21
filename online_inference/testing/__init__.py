import requests
from os.path import isfile

TMP_DIR_NAME = "tmp/"
SAMPLE_PICKLE_PATH = "data/log-reg.pkl"

artifact_present = isfile(SAMPLE_PICKLE_PATH)


def inet_avaliable(timeout: int = 1) -> bool:
    try:
        requests.head("http://www.google.com/", timeout=timeout)
        return True
    except requests.ConnectionError:
        return False


online = inet_avaliable()
