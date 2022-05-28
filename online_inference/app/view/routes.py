import json
from flask import Blueprint, jsonify, redirect, url_for, request

from .helper import (
    operating,
    empty_response,
    healthy_response,
    prediction_response,
    validate_payload,
)
from .. import default_logger
from ..utils.inference import make_prediction

log = default_logger(__name__)

api = Blueprint("api", __name__)


@api.route("/health", methods=["GET"])
def health_handler() -> str:
    log.info(msg="Application status requested")
    return healthy_response() if operating() else empty_response()


@api.route("/predict", methods=["GET"])
def predict_handler() -> str:
    log.info(msg="Prediction requested")
    if not operating():
        log.warning(msg="App is not set up correctly")
        return redirect(url_for(".health_handler"))
    if "payload" not in request.values:
        log.warning(msg="No payload in request")
        return jsonify(prediction_response(None))

    try:
        payload = json.loads(request.values["payload"])
    except json.JSONDecodeError:
        log.warning(msg="Payload should be an encoded JSON string")
        return jsonify(prediction_response(None))

    log.debug(msg="Sends prediction response")
    if not validate_payload(payload):
        log.warning(msg="Seems like the input did not pass validation")
        return jsonify(prediction_response(None))

    prediction = make_prediction(payload).tolist()
    return jsonify(prediction_response(prediction))


@api.errorhandler(404)
@api.route("/404")
def page_not_found_redirect(e=None) -> str:
    return "<h1>Page not found</h1>"
