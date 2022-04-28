from dataclasses import dataclass
import json
import pickle
import logging

import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    precision_score,
    accuracy_score,
    recall_score,
    f1_score,
)

from settings.training_params import EstimatorConfig


log = logging.getLogger(__name__)


@dataclass
class Report:
    accuracy: float
    recall: float
    precision: float
    f1: float

    def dump(self, path: str) -> None:
        log.debug(msg=f"Dumping metrics to {path}")
        with open(path, "w+") as f:
            json.dump(self.__dict__, f)


def get_metrics(
    true_target: pd.Series or np.ndarray,
    prediction: np.ndarray,
    params: EstimatorConfig,
) -> Report:
    # required as the model is trained on probably non-numeric labels
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
