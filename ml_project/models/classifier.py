import pickle
from typing import NoReturn, Union, Dict, Any
import logging
from os import getenv
from dataclasses import dataclass

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (
    GradientBoostingClassifier,
    HistGradientBoostingClassifier,
)
from sklearn.metrics import (
    precision_score,
    accuracy_score,
    recall_score,
    f1_score,
)
# from sklearn.pipeline import Pipeline, make_pipeline


def _make_logger(name: str) -> logging.Logger:

    log = logging.getLogger(name)

    if not log.hasHandlers():
        DEBUGLEVEL = getenv("DEBUG_LEVEL", "DEBUG")
        log.disabled = getenv("WRITE_LOGS", "True") == "False"

        log.setLevel(getattr(logging, DEBUGLEVEL))

        logging.basicConfig(
            format="[%(asctime)s]::[%(name)s]::[%(levelname)s]::%(message)s",
            datefmt="%D # %H:%M:%S",
        )

    return log


log = _make_logger(__name__)

Estimator = Union[
    LogisticRegression,
    RandomForestClassifier,
    GradientBoostingClassifier,
    HistGradientBoostingClassifier,
]

IMPLEMENTED_MODELS = dict(
    LogReg=LogisticRegression,
    RandomForest=RandomForestClassifier,
    Boosting=GradientBoostingClassifier,
    HistBoosting=HistGradientBoostingClassifier,
)


def make_estimator(
    features: pd.DataFrame,
    target: pd.Series,
    random_state: int,
    model_type: str,
    model_kwds: Dict[str, Any]
) -> Estimator:
    """
    Instantiates estimator class and fits it
    on given data

    :param features, DataFrame or np.ndarray
    :param target, Series or np.ndarray
    :param random_state, int
    :param model_type, str - model type, must be implemented
    (see `IMPLEMENTED_MODELS`)
    :param model_kwds, Dict[str, Any] - keywords to build a model

    :rtype Estimator, model instance
    """
    log.debug(msg="Creating estimator")
    if model_type not in IMPLEMENTED_MODELS.keys():
        error_message = f"Invalid model type: {model_type}"
        log.error(msg=error_message)
        raise ValueError(error_message)
    try:
        model = IMPLEMENTED_MODELS[model_type]
        model = model(**model_kwds, random_state=random_state)
    except (ValueError, TypeError) as e:
        log.error(msg="Invalid model args")
        log.error(exc_info=e)
        raise e
    log.debug(msg=f"Fitting {type(model)}")
    model.fit(features, target)
    log.debug(msg="Fitting complete")
    return model


@dataclass
class Report:
    accuracy: float
    recall: float
    precision: float
    f1: float


def get_metrics(
    true_target: pd.Series or np.ndarray,
    prediction: np.ndarray
) -> Report:
    metrics = {
        "accuracy": accuracy_score(true_target, prediction),
        "recall": recall_score(true_target, prediction),
        "precision": precision_score(true_target, prediction),
        "f1": f1_score(true_target, prediction)
    }
    return Report(**metrics)


def dump_model(model: Estimator, dump_to: str) -> NoReturn:
    log.debug(msg=f"Serializing model to {dump_to}")

    try:
        with open(dump_to, "wb+") as f:
            pickle.dump(model, f)
    except (FileNotFoundError, pickle.PicklingError) as e:
        log.error(msg="Failed to serialize model")
        log.error(exc_info=e)
        raise e

    log.debug(msg="Dump complete")
