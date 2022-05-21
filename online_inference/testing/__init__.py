import requests

TMP_DIR_NAME = "tmp/"


def inet_avaliable(timeout: int = 1) -> bool:
    try:
        requests.head("http://www.google.com/", timeout=timeout)
        return True
    except requests.ConnectionError:
        return False


online = inet_avaliable()
