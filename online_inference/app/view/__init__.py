from .. import AppConfig, default_logger

log = default_logger(__name__)


def application_factory(settings: AppConfig):
    """Creates and configures application instanse"""
    log.info(msg="Creates application instanse")

    from .routes import app
    from ..utils import load_artifact

    with app.app_context():
        artifact = load_artifact(settings.artifact_path)
        if artifact:
            app.config["HEALTHY"] = True
            app.config["MODEL"] = artifact

        log.info(msg="Application configured")
        return app
