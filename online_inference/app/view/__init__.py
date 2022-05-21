from flask import Flask

from .. import AppConfig, default_logger

log = default_logger(__name__)


def application_factory(settings: AppConfig) -> Flask:
    """
    Creates and configures application instance

    :param settings - AppConfig

    :rtype - Flask object
    """
    log.info(msg="Creates application instance")

    app = Flask(__name__)

    from .routes import api
    from ..utils import on_startup

    app.register_blueprint(api)

    with app.app_context():
        if on_startup(settings):
            # startup routines worked out correctly
            log.debug(msg="All items collected, updating current app's config")
            app.config["HEALTHY"] = True
            log.debug(msg="Startup routines done")

        log.info(msg="Application configured")
        return app
