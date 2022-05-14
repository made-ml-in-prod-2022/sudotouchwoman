from typing import List, Optional, Dict, Union
from flask import current_app

import pandas as pd

from .. import default_logger
from ..utils.validate import table_structure_validation, outlier_validation

log = default_logger(__name__)


def operating() -> bool:
    with current_app.app_context():
        return "HEALTHY" in current_app.config.keys()


def empty_response():
    return dict(status=400, body=None)


def healthy_response():
    return dict(status=200)


def prediction_response(prediction: Optional[List]):
    return dict(status=200, body=dict(prediction=prediction))


def validate_payload(payload: List[Dict[str, Union[str, float]]]) -> bool:
    log.debug(msg="Performs payload validation")
    log.debug(msg=f"Payload: {payload}")

    try:
        payload = pd.DataFrame(data=payload)
    except (ValueError, TypeError) as e:
        log.error(msg="Failed to build DataFrame from payload")
        log.error(msg=f"{e}")
        return False

    schema = current_app.config["TABLE_SCHEMA"]
    try:
        table_structure_validation(payload, schema, raises=True)
        log.debug(msg="Column structure matched, OK")
    except ValueError:
        log.error(msg="Column structure validation failed")
        return False

    # the payload is of correct format, check
    # distribution quality
    stats = current_app.config["STATS"]
    try:
        mean, std = stats[0], stats[1]
        outlier_validation(payload.values, mean=mean, std=std, raises=True)
        log.debug(msg="Outlier check passed")
    except ValueError:
        log.warning(msg="Found some outliers")

    log.debug(msg="Payload validation done")
    return True
