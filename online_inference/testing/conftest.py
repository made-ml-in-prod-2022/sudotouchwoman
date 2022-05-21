from typing import Dict, List
from os import mkdir, remove
from os.path import isdir

import pytest

from . import TMP_DIR_NAME, SAMPLE_PICKLE_PATH
from .mocks import testing_artifact, testing_stats, testing_schema


@pytest.fixture
def table_format() -> Dict[str, List[str]]:
    return dict(
        columns=["numeric", "categorical"],
        numeric_columns=["numeric"],
        categorical_columns=["categorical"],
    )


@pytest.fixture
def testing_application_config() -> Dict[str, str]:
    """
    The resources for application to operate are
    collected from the default sample locations (these
    are included into the git repo)

    :rtype - Dict[str, str] - AppConfig kwargs
    """
    return dict(
        artifact_path=SAMPLE_PICKLE_PATH,
        table_schema_path="configs/tabular-schema.json",
        feature_stats_path="configs/statistics.json",
    )


@pytest.fixture
def invalid_application_config() -> Dict[str, str]:
    """
    Works like `testing_appication_config`, but
    the keywords have invalid values. Given that, the application
    should abort the startup and respond as unhealthy

    :rtype: Dict[str, str]
    """
    return dict(
        artifact_path=None,
        table_schema_path=None,
        feature_stats_path=None,
    )


@pytest.fixture
def tmp_application_config(table_format: Dict[str, str]) -> Dict[str, str]:
    """
    Fixture creates temporary files for mocked configs
    Application configured with such data should
    startup correctly

    :rtype: Dict[str, str] - keyword-arguments for AppConfig
    """
    # startup: create temporary files with resources
    # tmp dir should be created at module scope for testing routines
    tmp = TMP_DIR_NAME
    mkdir(tmp) if not isdir(tmp) else None

    # this one is a bit tricky: application expects the artifact
    # to be a filename to pickle dump with actual Pipeline instance
    # thus for testing, a temporary dump should be created with
    # some dummy artifact to pass validation during startup

    # this way, filenames are passed through helper functions
    # via pipeline pattern (see `.mocks` module for more insights)
    tmp_resources = dict(
        artifact_path=testing_artifact("tmp/artifact.pkl"),
        table_schema_path=testing_schema("tmp/schema.json", table_format),
        feature_stats_path=testing_stats("tmp/statistics.json"),
    )

    yield tmp_resources

    # teardown: remove temporary files
    for file in tmp_resources.values():
        remove(file)
