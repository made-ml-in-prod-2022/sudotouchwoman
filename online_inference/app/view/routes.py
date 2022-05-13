from flask import Flask, current_app

from .. import default_logger

log = default_logger(__name__)

app = Flask(__name__, instance_relative_config=True)


@app.route("/health", methods=["GET"])
def health_handler() -> str:
    log.info(msg="Application status requested")
    return "200" if "HEALTHY" in current_app.config.keys() else "400"


@app.errorhandler(404)
@app.route("/404")
def page_not_found_redirect(e=None) -> str:
    return "<h1>Page not found</h1>"
