import logging
from os import getenv
from typing import List, Tuple, Union

import pandas as pd

from sklearn.model_selection import train_test_split


__all__ = ["extract_target", "extract_feature_columns", "split_data"]


def _make_logger(name: str) -> logging.Logger:

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


log = _make_logger(__name__)


def extract_target(data: pd.DataFrame, target_column: str) -> pd.Series:
    log.debug(
        msg=f"Extracting target variable from pandas table: {target_column}"
    )
    try:
        target = data[target_column]
    except ValueError as e:
        log.error(msg=f"Column must be missing: {target_column}")
        raise e
    return target


def extract_feature_columns(
    data: pd.DataFrame, feature_columns: List[str]
) -> pd.DataFrame:
    log.debug(msg=f"Extracting features from pandas table: {feature_columns}")
    try:
        features = data[feature_columns]
    except ValueError as e:
        log.error(msg=f"Some columns must be missing: {feature_columns}")
        raise e
    return features


def split_data(
    features: pd.DataFrame,
    target: pd.Series,
    test_size: Union[float, int],
    random_state: int,
) -> Tuple[Tuple[pd.DataFrame, pd.Series]]:
    log.debug(msg=f"Splitting the dataset ({test_size=})")
    return train_test_split(
        features,
        target,
        test_size=test_size,
        random_state=random_state,
        stratify=target
    )
