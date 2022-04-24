from typing import List, NoReturn

import logging
import requests
from os import getenv, mkdir
from os.path import isfile, isdir

import pandas as pd


def make_logger(name: str) -> logging.Logger:

    log = logging.getLogger(name)

    if not log.hasHandlers():
        DEBUGLEVEL = getenv("DEBUG_LEVEL", "DEBUG")
        log.disabled = getenv("WRITE_LOGS", "True") == "False"

        log.setLevel(getattr(logging, DEBUGLEVEL))

        logging.basicConfig(
            format="[%(asctime)s]::[%(name)s]::[%(levelname)s]::%(message)s",
            datefmt="%D # %H:%M:%S",
        )

    return log


log = make_logger(__name__)


def download_file(
    url: str, local_filename: str = None, overwrite: bool = False
) -> str:
    if not local_filename:
        *_, local_filename = url.split("/")
        log.debug(msg=f"No filename provided, will save as {local_filename}")

    if not overwrite and isfile(local_filename):
        log.info(msg=f"File already exists: {local_filename}")
        return local_filename

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, "wb+") as f:
            for chunk in r.iter_content():
                f.write(chunk)

    log.info(msg=f"File saved at {local_filename}")
    return local_filename


def create_dataset(
    source_url: str, target_dir: str, dataset_name: str
) -> NoReturn:
    if not isdir(target_dir):
        mkdir(target_dir)
        log.info(msg=f"Created dir for raw data: {target_dir}")

    dataset_filename = f"{target_dir}/{dataset_name}"
    download_file(source_url, dataset_filename, overwrite=False)


def read_dataset(
    dataset_path: str,
    column_names: List[str] or None,
    header: int or None,
) -> pd.DataFrame:
    if not isfile(dataset_path):
        log.error(msg=f"Dataset File not found: {dataset_path}")
        raise FileNotFoundError()

    if column_names is None and header is None:
        log.error(
            msg="Either set of column names or a header row should be provided"
        )
        raise TypeError("Column names not provided")

    log.debug(msg=f"Reading dataset from {dataset_path}")
    return pd.read_csv(dataset_path, header=header, names=column_names)
