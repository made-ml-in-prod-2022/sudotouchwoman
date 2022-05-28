import io
import json
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

import requests
import numpy as np
import pandas as pd

from validators import url

from .. import default_logger

log = default_logger(__name__)


@dataclass
class TabularDataSchema:
    """
    Container with column format for `DataFrame`
    validation on incoming `/predict` requests
    """

    columns: List[str]
    numeric_columns: List[str]
    categorical_columns: List[str]


def load_tabular_schema(
    source: Union[str, io.StringIO]
) -> Optional[TabularDataSchema]:
    """
    Loads configuration for TabularDataSchema
    in a JSON format. Returns `None` on error

    :param source, `str` or `io.StringIO` - resource location
    or buffer. Supports URLs and filenames

    :rtype `TabularDataSchema` or `None`
    """
    # deserialize JSON into tabular data schema (essentially
    # sets of columns) to later ensure incoming data
    log.debug(msg=f"Reading feature schema from {source}")
    if isinstance(source, str):
        try:
            if url(source):
                log.debug(msg="Collecting from specified URL")
                with requests.get(source) as response:
                    response.raise_for_status()
                    return TabularDataSchema(**json.loads(response.content))
            else:
                log.debug(msg="Collecting from local filesystem")
                with open(source, "r") as f:
                    return TabularDataSchema(**json.load(f))
        except (
            FileNotFoundError,
            json.JSONDecodeError,
            KeyError,
            TypeError,
            requests.HTTPError,
        ) as e:
            log.error(msg="Encountered error during schema loading")
            log.error(msg=f"{type(e)}")
            log.error(msg=f"{e}")
            return

    if isinstance(source, io.StringIO):
        try:
            return TabularDataSchema(**json.load(source))
        except (json.JSONDecodeError, KeyError) as e:
            log.error(msg="Encountered error during schema loading")
            log.error(msg=f"{e}")
            return
    log.error(msg=f"Unknown source type: {type(source)}")
    return


def load_stats(source: str, /) -> Optional[Tuple[np.ndarray, np.ndarray]]:
    """
    Collect mean and std for numerical features obtained
    earlier on train data to perform outlier detection

    :param source, str - path/URL to a valid JSON

    :rtype `tuple` with 2 `np.ndarray` (mean & std, respectively)
    or `None` if errors occured
    """
    log.debug(msg=f"Reading statistical data from {source}")

    try:
        if url(source):
            log.debug(msg="Collecting from specified URL")
            with requests.get(source) as response:
                response.raise_for_status()
                stats = json.loads(response.content)
        else:
            log.debug(msg="Collecting from local filesystem")
            with open(source, "r") as f:
                stats = json.load(f)
        log.debug(msg="Read JSON data")

        if len(stats["mean"]) != len(stats["std"]):
            log.error(msg="Make sure that the input is consistent")
            raise ValueError

        return np.array(stats["mean"]), np.array(stats["std"])

    except (
        json.JSONDecodeError,
        FileNotFoundError,
        KeyError,
        ValueError,
        TypeError,
        requests.HTTPError,
    ) as e:
        log.error(msg="Encountered error during stats loading")
        log.error(msg=f"{type(e)}")
        log.error(msg=f"{e}")
        return


def table_structure_validation(
    data: pd.DataFrame,
    schema: TabularDataSchema,
    *,
    raises: bool = False,
) -> bool:
    """
    Validate `DataFrame` using `TabularDataSchema`

    :param data, `pd.DataFrame` - df to check
    :param schema, `TabularDataSchema` to refer to
    :param raises, `bool` - whether to raise `TypeError` on
    validation failure. Default `False`.

    :rtype `bool`
    """
    log.debug(msg="Checking incoming DataFrame structure")
    all_cols = data.columns.tolist()
    numeric_cols = data.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = data.select_dtypes(include=["object"]).columns.tolist()

    if len(all_cols) != len(set(all_cols)):
        log.warning(msg="Duplicate columns are not allowed")
        if not raises:
            return False
        raise ValueError("Duplicate columns")

    if all_cols != schema.columns:
        log.warning(msg="Columns format validation aborted")
        log.warning(msg=f"Expected {set(schema.columns)}")
        log.warning(msg=f"found {set(all_cols)}")
        if not raises:
            return False
        raise ValueError("Column format mismatch")

    if numeric_cols != schema.numeric_columns:
        log.warning(msg="Numeric columns validation aborted")
        log.warning(msg=f"Expected {set(schema.numeric_columns)}")
        log.warning(msg=f"found {set(numeric_cols)}")
        if not raises:
            return False
        raise ValueError("Numeric columns mismatch")

    if categorical_cols != schema.categorical_columns:
        log.warning(msg="Categorical columns validation aborted")
        log.warning(msg=f"Expected {set(schema.categorical_columns)}")
        log.warning(msg=f"Found {set(categorical_cols)}")
        if not raises:
            return False
        raise ValueError("Categorical columns mismatch")

    return True


def outlier_validation(
    data: np.ndarray,
    *,
    mean: np.ndarray,
    std: np.ndarray,
    sigma_range: int = 3,
    raises: bool = False,
) -> bool:
    """
    Simple 6-sigma test with adjustable tolerance

    :param data `np.ndarray` to validate
    :param mean - `np.ndarray` with columnwise means
    :param std - `np.ndarray` with columnwise std
    :param raises - bool, whether to raise `TypeError`
    on validation failure. Default `False`.

    :rtype `bool`
    """
    log.debug(msg="Checking the data for ouliers")
    # perform simple sigma test (ensure that incoming data
    # approximately belongs to the original training data distribution)
    sigma_ranged = (mean - sigma_range * std > data) + (
        data > mean + sigma_range * std
    )

    if not sigma_ranged.any():
        log.debug(msg="6-sigma test passed")
        return True

    if not raises:
        return False
    raise ValueError("Sample data did not pass sigma test")
