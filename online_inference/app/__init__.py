import logging
from os import getenv, getpid
from dataclasses import dataclass

from flask import Flask

from dotenv import load_dotenv
from click import secho

ENV_PATH = getenv("ENV_PATH")

if ENV_PATH:
    secho(f"Loading environment from {ENV_PATH}", fg="green")
    load_dotenv(ENV_PATH)
else:
    secho("User-defined environment not set", fg="yellow")

# bind logfile names to pid to
# let multiple workers write into separate files
LOGFILE = f'{getenv("LOGFILE", "server")}-{getpid()}.log'


@dataclass
class AppConfig:
    """
    Config with paths to resource locations:
    values are collected from environmental variables by default

    artifact_path: str
    table_schema_path: str
    feature_stats_path: str
    """

    artifact_path: str = getenv("ARTIFACT", None)
    table_schema_path: str = getenv("TABLE_SCHEMA", None)
    feature_stats_path: str = getenv("STATS", None)


def make_logger(name: str, logfile: str) -> logging.Logger:
    log = logging.getLogger(name)

    if not log.hasHandlers():
        LOGLEVEL = getenv("LOG_LEVEL", "DEBUG")
        log.setLevel(getattr(logging, LOGLEVEL.upper()))

        formatter = logging.Formatter(
            "[%(asctime)s]::[%(levelname)s]::[%(name)s]::%(message)s",
            "%D # %H:%M:%S",
        )

        if getenv("LOG_FILE", "False") == "True":
            file = logging.FileHandler(filename=f"{logfile}", encoding="utf-8")
            file.setFormatter(formatter)
            log.addHandler(file)

        if getenv("LOG_STREAM", "False") == "True":
            stream = logging.StreamHandler()
            stream.setFormatter(formatter)
            log.addHandler(stream)

    return log


def default_logger(name: str) -> logging.Logger:
    return make_logger(name, LOGFILE)


log = default_logger(__name__)


def make_app(settings: AppConfig = AppConfig()) -> Flask:
    from .view import application_factory

    log.info(msg="Application is in the oven")
    log.info(msg=f"Recieved application config: {settings}")
    app = application_factory(settings=settings)
    return app
