from flask import current_app

from .inference import load_artifact, validate_artifact
from .validate import load_tabular_schema, load_stats

from .. import AppConfig, default_logger

log = default_logger(__name__)


def on_startup(settings: AppConfig) -> bool:
    """
    Startup routine: try to collect application resources:

    + model artifact
    + input data format for requests
    + statistics

    :param settings, `AppConfig`

    :rtype `bool`
    """
    with current_app.app_context():
        log.info(msg="Running startup routine")
        log.debug(msg="Collecting model artifact")

        artifact = load_artifact(settings.artifact_path)
        if not validate_artifact(artifact):
            log.critical(msg="Failed to load artifact, aborting startup")
            return False

        table_schema = load_tabular_schema(settings.table_schema_path)
        if not table_schema:
            log.critical(msg="Failed to load table schema, aborting startup")
            return False

        stats = load_stats(settings.feature_stats_path)
        if not stats:
            msg = "Failed to load statistics for features, aborting statrup"
            log.critical(msg=msg)
            return False

        current_app.config["ARTIFACT"] = artifact
        current_app.config["TABLE_SCHEMA"] = table_schema
        current_app.config["STATS"] = stats
    return True
