from typing import Tuple
from os import mkdir, remove, walk
from os.path import isfile, isdir, join
from requests import ConnectionError

import pytest
import pandas as pd

from src.data.datautils import download_file, create_dataset, read_dataset
from src.settings.params import DatasetConfig
from testing.utils import online, TMP_DIR_NAME


def setup_module(module):
    tmp = TMP_DIR_NAME
    mkdir(tmp) if not isdir(tmp) else None


def teardown_module(module):
    tmp = TMP_DIR_NAME
    for root, _, files in walk(tmp):
        for file in files:
            remove(join(root, file))


@pytest.fixture
def downloadable_links() -> Tuple[str]:
    # pylint shouts at me if the lines are 1 character longer than 79
    # you know what pylint eff you
    return (
        "".join(
            (
                "https://github.com/",
                "sudotouchwoman/park_sem1_ML",
                "/blob/master/wdbc.data",
                "?raw=true",
            )
        ),
        "".join(
            (
                "https://github.com/",
                "sudotouchwoman/park_sem1_ML",
                "/blob/master/wdbc.names",
                "?raw=true",
            )
        ),
    )


def test_download_file(downloadable_links):
    # this test ensures that the download is performed
    # and at least, networking error occures
    # other tests require internet connection to operate
    # thus are skipped in case we are not online
    assert isdir(TMP_DIR_NAME)

    for i, link in enumerate(downloadable_links):
        filename = f"{TMP_DIR_NAME}/blob-{i}"
        remove(filename) if isfile(filename) else None

        assert isinstance(link, str)
        try:
            download_file(link, filename, overwrite=False)
            assert isfile(filename)
        except Exception as e:
            # there may be no internet connection
            # in this case, we ensure that the exception
            # raised is dedicated to this
            assert isinstance(e, ConnectionError)


@pytest.fixture
def valid_ds_conf(downloadable_links: Tuple[str]) -> DatasetConfig:
    return DatasetConfig(
        # how should I test such things properly?
        source_url=downloadable_links[0],
        dataset_dir=TMP_DIR_NAME,
        dataset_filename="wdbc.data",
        download=False,
        header=0,
    )


@pytest.mark.skipif(not online, reason="Must be online to download files")
def test_create_dataset(valid_ds_conf):
    # ensure typing
    assert isinstance(valid_ds_conf, DatasetConfig)

    # if the file is present before test, remove it
    full_path = f"{valid_ds_conf.dataset_dir}/{valid_ds_conf.dataset_filename}"
    remove(full_path) if isfile(full_path) else None

    # with download=False, the dataset file should not appear
    valid_ds_conf.download = False
    create_dataset(valid_ds_conf)
    assert not isfile(full_path)

    # if download=True, the file must be fetched
    valid_ds_conf.download = True
    create_dataset(valid_ds_conf)
    assert isfile(full_path)


@pytest.mark.skipif(not online, reason="Must be online to download files")
def test_read_dataset(valid_ds_conf):
    # ensure typing
    assert isinstance(valid_ds_conf, DatasetConfig)

    # if we came this far, this means that the
    # dataset file should be present in tmp/... location
    full_path = f"{valid_ds_conf.dataset_dir}/{valid_ds_conf.dataset_filename}"
    assert isfile(full_path)

    dataset = read_dataset(valid_ds_conf)
    assert isinstance(dataset, pd.DataFrame)
    assert dataset.shape[0] > 50
    assert dataset.columns.tolist() == valid_ds_conf.column_names
