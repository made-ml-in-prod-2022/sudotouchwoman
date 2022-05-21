from flask import current_app

from .inference import load_artifact, validate_artifact
from .validate import load_tabular_schema, load_stats

from .. import AppConfig, default_logger

log = default_logger(__name__)


def on_startup(settings: AppConfig) -> bool:
    with current_app.app_context():
        log.debug(msg="Running startup routine")
        log.debug(msg="Collecting model artifact")

        artifact = load_artifact(settings.artifact_path)
        if not validate_artifact(artifact):
            log.fatal(msg="Failed to load artifact, aborting startup")
            return False

        table_schema = load_tabular_schema(settings.table_schema_path)
        if not table_schema:
            log.fatal(msg="Failed to load table schema, aborting startup")
            return False

        stats = load_stats(settings.feature_stats_path)
        if not stats:
            msg = "Failed to load statistics for features, aborting statrup"
            log.fatal(msg=msg)
            return False

        current_app.config["ARTIFACT"] = artifact
        current_app.config["TABLE_SCHEMA"] = table_schema
        current_app.config["STATS"] = stats
    return True