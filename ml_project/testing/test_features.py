from itertools import chain
from typing import List

import pytest
from pytest_mock import MockerFixture

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from features.extract import (
    extract_feature_columns,
    extract_target,
    split_data,
    SplitConfig,
)

from features.process import (
    numeric_features_transform,
    # categorical_features_transform,
    # preprocessing_pipeline,
)

from settings.features_params import FeaturesConfig


@pytest.fixture
def cat_columns() -> List[str]:
    return [f"cat-feature-{i}" for i in range(5)]


@pytest.fixture
def num_columns() -> List[str]:
    return [f"num-feature-{i}" for i in range(5)]


@pytest.fixture
def target_column() -> str:
    return "target"


@pytest.fixture
def missing_columns() -> List[str]:
    return ["missing", "not-in-df"]


@pytest.fixture
def sample_data(
    cat_columns: List[str], num_columns: List[str], target_column: str
) -> pd.DataFrame:
    rng = np.random.default_rng(seed=10)
    mu, sigma = 0.0, 2e-1
    items = 20

    values = chain(
        ((rng.normal(mu, sigma, items)) for _ in num_columns),
        (str(rng.normal(mu, sigma, items)) for _ in cat_columns),
        (rng.choice(2, size=items, replace=True),),
    )
    columns = (*num_columns, *cat_columns, target_column)
    data = {col: value for col, value in zip(columns, values)}

    return pd.DataFrame(data)


def test_extract_target(sample_data: pd.DataFrame, target_column: str):
    assert isinstance(sample_data, pd.DataFrame)
    assert isinstance(target_column, str)

    assert sample_data[target_column] is not None

    target = extract_target(sample_data, target_column)
    assert isinstance(target, pd.Series)

    not_in_df = "non-existent-column"
    assert not_in_df not in sample_data

    with pytest.raises(KeyError) as exc_info:
        extract_target(sample_data, not_in_df)

    exception_raised = exc_info.value
    assert isinstance(exception_raised, KeyError)


def test_extract_feature_columns(
    sample_data: pd.DataFrame,
    num_columns: List[str],
    cat_columns: List[str],
):
    assert isinstance(sample_data, pd.DataFrame)

    must_be_num = extract_feature_columns(sample_data, num_columns)
    assert isinstance(must_be_num, pd.DataFrame)

    for column in must_be_num:
        # this is quite an awkward way of type-checking
        # but .dtype of both Series and ndarray objects
        # is essentially a property, not np.float or str
        assert isinstance(must_be_num[column], pd.Series)
        assert isinstance(must_be_num[column].sum(), np.float64)

    # there could have been a ripndip reference
    must_be_cat = extract_feature_columns(sample_data, cat_columns)
    assert isinstance(must_be_cat, pd.DataFrame)

    for column in must_be_cat:
        assert isinstance(must_be_cat[column], pd.Series)
        assert isinstance(must_be_cat[column].sum(), str)


def test_logger_calls(
    sample_data: pd.DataFrame,
    missing_columns: List[str],
    mocker: MockerFixture,
):
    mock_logger = mocker.stub()
    mocker.patch("features.extract.log.error", mock_logger)

    with pytest.raises(KeyError) as exc_info:
        # must be missing and raise
        extract_feature_columns(sample_data, missing_columns)

    exception_raised = exc_info.value
    assert isinstance(exception_raised, KeyError)

    expected_err = f"Some columns must be missing: {missing_columns}"
    mock_logger.assert_called_once_with(msg=expected_err)


@pytest.fixture
def split_params() -> SplitConfig:
    return SplitConfig(validation=0.5)


def test_split_data(
    sample_data: pd.DataFrame,
    num_columns: List[str],
    cat_columns: List[str],
    target_column: str,
    split_params: SplitConfig,
):
    feature_columns = num_columns + cat_columns
    features = extract_feature_columns(sample_data, feature_columns)
    target = extract_target(sample_data, target_column)

    split = split_data(features, target, split_params)
    assert isinstance(split, list)

    # validation size is set to 50%
    # thus the training and validation sets should be
    # of equal shapes
    train_x, val_x, train_y, val_y = split
    rows, cols = features.shape
    assert train_x.shape == val_x.shape == (rows // 2, cols)
    assert train_y.shape == val_y.shape == (rows // 2,)

    # ensure the stratification
    # note that in this example has 2 classes thus
    # classes are either equally balanced or 1 item is odd somewhere
    diff = np.count_nonzero(train_y) - np.count_nonzero(val_y)
    assert diff in (-1, 0, 1)


@pytest.fixture
def features_conf(
    num_columns: List[str], cat_columns: List[str], target_column: str
) -> FeaturesConfig:
    # config with most default values to test
    # transforms
    return FeaturesConfig(
        target=target_column,
        categorical_features=cat_columns,
        numeric_features=num_columns,
    )


@pytest.fixture
def numeric_data() -> np.ndarray:
    # some data to test numeric transform
    rng = np.random.default_rng()
    return rng.uniform(size=(10, 50))


def test_numeric_features_transform(
    numeric_data: np.ndarray,
    features_conf: FeaturesConfig,
    mocker: MockerFixture,
):
    # spy logger calls
    mock_logger = mocker.stub()
    mocker.patch("features.process.log.error", mock_logger)

    # this call with default settings is fine
    num_transformer = numeric_features_transform(features_conf.scaler_type)
    assert isinstance(num_transformer, Pipeline)
    mock_logger.assert_not_called()

    # without PCA, output shape should match input shape
    transformed = num_transformer.fit_transform(numeric_data)
    assert isinstance(transformed, np.ndarray)
    assert numeric_data.shape == transformed.shape

    # attempt to pass invalid scaler type
    with pytest.raises(ValueError) as exc_info:
        numeric_features_transform("non-existing-scaler")

    exception_raised = exc_info.value
    assert isinstance(exception_raised, ValueError)
    mock_logger.assert_called_once()
