from .. import AppConfig, default_logger

log = default_logger(__name__)


def application_factory(settings: AppConfig):
    """Creates and configures application instance"""
    log.info(msg="Creates application instance")

    from .routes import app
    from ..utils import on_startup

    with app.app_context():
        if on_startup(settings):
            # startup routines worked out correctly
            log.debug(msg="All items collected, updating current app's config")
            app.config["HEALTHY"] = True
            log.debug(msg="Startup routines done")

        log.info(msg="Application configured")
        return app
