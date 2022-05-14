import logging
from os import getenv
from dataclasses import dataclass

from flask import Flask

# from dotenv import load_dotenv
# from click import secho

# ENV_PATH = getenv("ENV_PATH")

# if ENV_PATH:
#     secho(f"Loading environment from {ENV_PATH}", fg="green")
#     load_dotenv(ENV_PATH)
# else:
#     secho("User-defined environment not set", fg="yellow")

LOGFILE = getenv("LOGFILE", "server.log")


@dataclass
class AppConfig:
    # host: str = getenv("HOST", "127.0.0.1")
    # port: int = getenv("PORT", "5000")
    # debug: bool = getenv("DEBUG", "True") == "True"
    artifact_path: str = getenv("ARTIFACT", None)
    table_schema_path: str = getenv("TABLE_SCHEMA", None)
    feature_stats_path: str = getenv("STATS", None)


def make_logger(name: str, logfile: str) -> logging.Logger:
    log = logging.getLogger(name)

    if not log.hasHandlers():
        DEBUGLEVEL = getenv("DEBUG_LEVEL", "DEBUG")

        log.disabled = getenv("LOG_ON", "True") == "False"
        log.setLevel(getattr(logging, DEBUGLEVEL))

        formatter = logging.Formatter(
            "[%(asctime)s]::[%(levelname)s]::[%(name)s]::%(message)s",
            "%D # %H:%M:%S",
        )
        handler = logging.FileHandler(filename=f"{logfile}", encoding="utf-8")
        handler.setFormatter(formatter)
        log.addHandler(handler)

    return log


def default_logger(name: str) -> logging.Logger:
    return make_logger(name, LOGFILE)


log = default_logger(__name__)


def make_app(s: AppConfig = AppConfig()) -> Flask:
    from .view import application_factory

    log.info(msg=f"Recieved application config: {s}")
    app = application_factory(settings=s)
    return app
