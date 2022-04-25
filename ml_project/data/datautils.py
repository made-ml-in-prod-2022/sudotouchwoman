from os import mkdir
from os.path import isfile, isdir
import logging
import requests

import pandas as pd

from settings.data_params import DatasetConfig

log = logging.getLogger(__name__)


def download_file(
    url: str, local_filename: str = None, overwrite: bool = False
) -> str:
    """
    Downloads file from given url.
    Check if such file is present before requesting

    :param url, str - web resource to fetch the file from
    :param local_filename, str (default None) -
    filename to save the file to.
    If not specified, the filename is deduced from the url
    :param overwrite, bool (default False) - whether to override the
    existing file

    :rtype str, local filename of the obtained resource
    """
    if not local_filename:
        *_, local_filename = url.split("/")
        log.warning(msg=f"No filename provided, will save as {local_filename}")

    if not overwrite and isfile(local_filename):
        log.warning(msg=f"File already exists: {local_filename}")
        return local_filename

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, "wb+") as f:
            for chunk in r.iter_content():
                f.write(chunk)

    log.info(msg=f"File saved at {local_filename}")
    return local_filename


def create_dataset(params: DatasetConfig) -> None:
    """
    Check whether the dataset file is present,
    download the file, if required

    :param params, DatasetConfig with required settings
    """
    if not isdir(params.dataset_dir):
        mkdir(params.dataset_dir)
        log.info(msg=f"Created dir for raw data: {params.dataset_dir}")

    dataset_filename = f"{params.dataset_dir}/{params.dataset_filename}"
    download_file(params.source_url, dataset_filename, overwrite=False)


def read_dataset(params: DatasetConfig) -> pd.DataFrame:
    dataset_path = f"{params.dataset_dir}/{params.dataset_filename}"
    log.debug(msg=f"Trying to open dataset at {dataset_path}")

    if not isfile(dataset_path):
        log.error(msg=f"Dataset File not found: {dataset_path}")
        raise FileNotFoundError()

    if params.column_names is None and params.header is None:
        log.error(
            msg="Either set of column names or a header row should be provided"
        )
        raise TypeError("Column names not provided")

    log.debug(msg=f"Reading dataset from {dataset_path}")
    return pd.read_csv(
        dataset_path, header=params.header, names=params.column_names
    )
