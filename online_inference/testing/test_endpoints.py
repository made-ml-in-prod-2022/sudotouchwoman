from typing import Dict, Iterable
from itertools import chain
import json

import pytest

from app import AppConfig, make_app
from . import artifact_present


@pytest.fixture
def invalid_queries(testing_payload: str) -> Iterable[Dict[str, str]]:
    invalid_columns = json.dumps(
        [{"invalid_entry": "invalid value"} for _ in (1, 2)]
    )
    invalid_format = json.dumps(testing_payload.strip("[]"))
    invalid_queries = {"arg": "value"}, {}, {"payld": testing_payload}
    return chain(
        map(lambda q: dict(payload=q), (invalid_columns, invalid_format)),
        invalid_queries,
    )


@pytest.mark.skipif(not artifact_present, reason="Requires model artifact")
def test_predict_endpoint(
    testing_application_config, testing_payload, invalid_queries
):
    app = make_app(AppConfig(**testing_application_config))

    with app.test_client() as c:
        # app should be running and healthy
        # to pass this test
        response = c.get("/health")
        assert response.status_code == 200
        assert b'{"status":200}' in response.data

        # test with several invalid payload examples
        # ensure that the server has no internal errors
        # and replies with "prediction": null to incorrect requests
        for query_string in invalid_queries:
            response = c.get("/predict", query_string=query_string)

            assert response.status_code == 200
            assert b'"status":200' in response.data
            assert b'"prediction":null' in response.data

        # test with correct payload format
        query_string = {"payload": testing_payload}
        response = c.get("/predict", query_string=query_string)

        # is it possible to avoid hardcoding the expected prediction?
        assert b'"status":200' in response.data
        assert b"prediction" in response.data
        assert b'"prediction":null' not in response.data
        assert b'"body":{"prediction":[' in response.data
