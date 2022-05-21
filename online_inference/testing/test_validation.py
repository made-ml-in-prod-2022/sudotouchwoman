from typing import Tuple

import pytest

import numpy as np
import pandas as pd

from app.utils.validate import (
    TabularDataSchema,
    table_structure_validation,
    outlier_validation,
)


def test_tabular_schema(table_format):
    schema = TabularDataSchema(**table_format)
    assert schema.columns == table_format["columns"]
    assert schema.numeric_columns == table_format["numeric_columns"]
    assert schema.categorical_columns == table_format["categorical_columns"]


@pytest.fixture
def some_stats() -> Tuple[float, float]:
    return 0.0, 1.0


@pytest.fixture
def sample_table(some_stats) -> pd.DataFrame:
    mean, std = some_stats
    rng = np.random.default_rng()
    return pd.DataFrame(
        {
            "numeric": rng.normal(loc=mean, scale=std, size=5),
            "categorical": map(str, np.linspace(-1, 11, 5)),
        }
    )


def test_table_structure_validation(table_format, sample_table):
    schema = TabularDataSchema(**table_format)
    assert table_structure_validation(sample_table, schema)

    # adding extra column which is not present in the schema
    # would fail structure validation
    with pytest.raises(ValueError) as exc_info:
        sample_table["invalid"] = np.zeros_like(sample_table.numeric)
        table_structure_validation(sample_table, schema, raises=True)

    exception_raised = exc_info.value
    assert isinstance(exception_raised, ValueError)


def test_outlier_validation(some_stats):
    # simple outlier test: check the original distribution
    # of data (here clamped std and shifted mean are used
    # in order to avoid pseudorandom (normal) crashes)
    rng = np.random.default_rng()
    mean, std = some_stats
    fine_data = rng.normal(mean, std / 4, size=10)
    outliers = rng.normal(mean + 10, 4 * std, size=30)

    assert outlier_validation(fine_data, mean=mean, std=std, raises=True)
    assert not outlier_validation(outliers, mean=mean, std=std, raises=False)

    # test possible options (both with and without raise)
    with pytest.raises(ValueError) as exc_info:
        outlier_validation(outliers, mean=mean, std=std, raises=True)

    exception_raised = exc_info.value
    assert isinstance(exception_raised, ValueError)
