from flask import Flask

from .. import default_logger

log = default_logger(__name__)

app = Flask(__name__, instance_relative_config=False)


def healthy() -> bool:
    with app.app_context():
        return "HEALTHY" in app.config.keys()


@app.route("/health", methods=["GET"])
def health_handler() -> str:
    log.info(msg="Application status requested")
    return "200" if healthy() else "400"


@app.errorhandler(404)
@app.route("/404")
def page_not_found_redirect(e=None) -> str:
    return "<h1>Page not found</h1>"
