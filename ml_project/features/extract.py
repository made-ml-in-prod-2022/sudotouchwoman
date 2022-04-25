from typing import List, Union
import logging

import pandas as pd
from sklearn.model_selection import train_test_split

from settings.data_params import SplitConfig

__all__ = ["extract_target", "extract_feature_columns", "split_data"]


log = logging.getLogger(__name__)


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
    params: SplitConfig,
) -> List[Union[pd.DataFrame, pd.Series]]:
    log.debug(msg=f"Splitting the dataset ({params.validation=})")
    return train_test_split(
        features,
        target,
        test_size=params.validation,
        random_state=params.random_state,
        stratify=target,
    )
