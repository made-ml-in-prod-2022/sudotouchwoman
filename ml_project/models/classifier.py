from typing import Union
from dataclasses import dataclass
import logging
import pickle

import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (
    GradientBoostingClassifier,
    HistGradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.metrics import (
    precision_score,
    accuracy_score,
    recall_score,
    f1_score,
)

from settings.training_params import EstimatorConfig


log = logging.getLogger(__name__)

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
    features: pd.DataFrame, target: pd.Series, params: EstimatorConfig
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
    if params.model_type not in IMPLEMENTED_MODELS.keys():
        error_message = f"Invalid model type: {params.model_type}"
        log.error(msg=error_message)
        raise ValueError(error_message)
    try:
        model = IMPLEMENTED_MODELS[params.model_type]
        model = model(**params.model_params)
    except (ValueError, TypeError) as e:
        log.error(msg="Invalid model args")
        log.error(msg=f"{e}")
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
    prediction: np.ndarray,
    params: EstimatorConfig,
) -> Report:
    pos_label = params.pos_label

    metrics = {
        "accuracy": accuracy_score(true_target, prediction),
        "recall": recall_score(true_target, prediction, pos_label=pos_label),
        "precision": precision_score(
            true_target, prediction, pos_label=pos_label
        ),
        "f1": f1_score(true_target, prediction, pos_label=pos_label),
    }
    return Report(**metrics)


def dump_pipeline(pipeline: Pipeline, dump_to: str) -> None:
    log.debug(msg=f"Serializing model to {dump_to}")

    try:
        with open(dump_to, "wb+") as f:
            pickle.dump(pipeline, f)
    except (FileNotFoundError, pickle.PicklingError) as e:
        log.error(msg="Failed to serialize model")
        log.error(msg=f"{e}")
        raise e

    log.debug(msg="Dump complete")


def make_inference_pipeline(
    preprocessor: Pipeline, estimator: Estimator
) -> Pipeline:
    # essentially clays together
    # the preprocessing pipeline
    # and the actual classifier
    # to be dumped as an artifact
    return make_pipeline(preprocessor, estimator)
