from typing import NoReturn
import logging
from logging.handlers import TimedRotatingFileHandler
from os import getenv
from dataclasses import dataclass

LOGFILE = getenv("LOGFILE", "app.log")


@dataclass
class AppConfig:
    host: str = getenv("HOST", "127.0.0.1")
    port: int = getenv("PORT", "5000")
    debug: bool = getenv("DEBUG", "True") == "True"
    artifact_path: str = getenv("ARTIFACT", None)


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
        handler = TimedRotatingFileHandler(
            filename=f"{logfile}", encoding="utf-8",
            interval=2, when=""
        )
        handler.setFormatter(formatter)
        log.addHandler(handler)

    return log


def default_logger(name: str) -> logging.Logger:
    return make_logger(name, LOGFILE)


def run(s: AppConfig) -> NoReturn:
    from .view import application_factory

    app = application_factory(settings=s)
    app.run(host=s.host, port=s.port, debug=s.debug)
