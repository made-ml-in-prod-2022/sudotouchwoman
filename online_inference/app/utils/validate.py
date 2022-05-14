import io
import json
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

import numpy as np
import pandas as pd

from .. import default_logger

log = default_logger(__name__)


@dataclass
class TabularDataSchema:
    columns: List[str]
    numeric_columns: List[str]
    categorical_columns: List[str]


def load_tabular_schema(
    source: Union[str, io.StringIO]
) -> Optional[TabularDataSchema]:
    # deserialize JSON into tabular data schema (essentially
    # sets of columns) to later ensure incoming data
    if isinstance(source, str):
        try:
            with open(source, "r") as f:
                return TabularDataSchema(**json.load(f))
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            log.error(msg="Encountered error during schema loading")
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
    log.debug(msg=f"Reading statistical data from {source}")

    try:
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
        TypeError
    ) as e:
        log.error(msg="Encountered error during stats loading")
        log.error(msg=f"{e}")
        return


def table_structure_validation(
    data: pd.DataFrame,
    schema: TabularDataSchema,
    *,
    raises: bool = False,
) -> bool:
    log.debug(msg="Checking incoming DataFrame structure")
    all_cols = data.columns.tolist()
    numeric_cols = data.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = data.select_dtypes(include=["object"]).columns.tolist()

    if len(all_cols) != len(set(all_cols)):
        log.warning(msg="Duplicate columns are not allowed")
        if not raises:
            return False
        raise ValueError("Duplicate columns")

    if set(numeric_cols) != set(schema.numeric_columns):
        log.warning(msg="Numeric columns validation aborted")
        log.warning(msg=f"Expected {set(schema.numeric_columns)}")
        log.warning(msg=f"found {set(numeric_cols)}")
        if not raises:
            return False
        raise ValueError("Numeric columns mismatch")

    if set(categorical_cols) != set(schema.categorical_columns):
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
    raises: bool = False,
) -> bool:
    log.debug(msg="Checking the data for ouliers")
    # perform simple sigma test (ensuer that incoming data
    # approximately belongs to the original training data distribution)
    sigma_ranged = mean - 3 * std <= data <= mean + 3 * std

    if sigma_ranged.all():
        log.debug(msg="6-sigma test passed")
        return True

    index, _ = np.where(sigma_ranged == 0)
    log.warning(msg=f"Detected outlier at positions {index}")
    if not raises:
        return False
    raise ValueError("Sample data did not pass sigma test")
