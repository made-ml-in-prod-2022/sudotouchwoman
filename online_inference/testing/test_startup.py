from typing import Tuple

import pytest

from app import make_app, AppConfig
from . import artifact_present


def test_app_config(testing_application_config):
    # check that the config instance is created
    # correctly and the attributes match
    cfg = AppConfig(**testing_application_config)

    assert cfg.artifact_path == testing_application_config["artifact_path"]
    assert (
        cfg.feature_stats_path
        == testing_application_config["feature_stats_path"]
    )
    assert (
        cfg.table_schema_path
        == testing_application_config["table_schema_path"]
    )


@pytest.fixture
def config_keys() -> Tuple[str]:
    return "ARTIFACT", "TABLE_SCHEMA", "STATS", "HEALTHY"


def test_invalid_startup(invalid_application_config, config_keys):
    app = make_app(AppConfig(**invalid_application_config))

    for property in config_keys:
        assert property not in app.config

    with app.test_client() as c:
        # if startup was aborted, app
        # should not respond with 200 on healthcheck
        response = c.get("/health")
        assert response.status_code == 200
        assert b'{"status":200}' not in response.data


@pytest.mark.parametrize(
    "config",
    [
        pytest.lazy_fixture("tmp_application_config"),
        # Note: used to fail in CI environment as there is no actual
        # pickle in data/ directory.
        # Fix: skipping test if the sample artifact is not found
        # Consider creating a pickle first
        # using pipeline.py in `ml_project` first
        # (this also applies to running the server)
        # and copying it to the desired location. Server should be
        # given a valid path to the binary to startup and operate
        pytest.lazy_fixture("testing_application_config"),
    ],
)
@pytest.mark.skipif(not artifact_present, reason="Model pickle not found")
def test_with_tmp_config(config, config_keys):
    # test that applicationn instance is created
    # with correct config values
    app = make_app(AppConfig(**config))

    # after correct startup, non-empty config entries
    # should be created to store model, input schema etc
    for property in config_keys:
        assert property in app.config
        assert app.config[property] is not None

    with app.test_client() as c:
        # app should be running and healthy
        response = c.get("/health")
        assert response.status_code == 200
        assert b'{"status":200}' in response.data
