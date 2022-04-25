import logging
from os import getenv
from typing import List

import pandas as pd
from sklearn.compose import make_column_transformer, ColumnTransformer
from sklearn.impute import SimpleImputer


__all__ = [
    "extract_target",
    "extract_feature_columns",
    "make_imputer"
]


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


def make_imputer(
    cat_features: List[str],
    num_features: List[str],
    num_imputer_strategy: str,
) -> ColumnTransformer:
    log.debug(msg="Creating imputer for missing values")
    num_imputer = SimpleImputer(strategy=num_imputer_strategy)
    cat_imputer = SimpleImputer(strategy="most_frequent")

    return make_column_transformer(
        (num_imputer, num_features), (cat_imputer, cat_features)
    )
