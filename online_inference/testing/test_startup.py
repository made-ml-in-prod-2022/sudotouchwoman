from os import mkdir, remove, walk
from os.path import isdir, join

import pytest
from app import make_app, AppConfig

from . import TMP_DIR_NAME


def setup_module(module):
    tmp = TMP_DIR_NAME
    mkdir(tmp) if not isdir(tmp) else None


def teardown_module(module):
    tmp = TMP_DIR_NAME
    for root, _, files in walk(tmp):
        for file in files:
            remove(join(root, file))


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


@pytest.mark.parametrize(
    "config",
    [
        pytest.lazy_fixture("testing_application_config"),
        pytest.lazy_fixture("invalid_application_config")
    ]
)
def test_application_factory(config):
    # test that applicationn instance is created
    # with correct config values
    cfg = AppConfig(**config)
    app = make_app(cfg)

    with app.test_client() as c:
        response = c.get("/health")
        assert response.status_code == 200
        assert b"status" in response.data


@pytest.mark.parametrize(
    "config",
    [
        pytest.lazy_fixture("tmp_application_config")
    ]
)
def test_with_tmp_config(config):
    # test that applicationn instance is created
    # with correct config values
    cfg = AppConfig(**config)
    app = make_app(cfg)

    with app.test_client() as c:
        response = c.get("/health")
        assert response.status_code == 200
        print(response.data)
        assert b"{\"status\":200}" in response.data
