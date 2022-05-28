import pickle
from typing import Optional, Union, List, Any

import requests
import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline
from validators import url

from flask import current_app

from .. import default_logger

log = default_logger(__name__)


def load_artifact(path: str) -> Optional[Pipeline]:
    log.debug(msg=f"Reading model artifact from {path}")
    try:
        if url(path):
            log.debug(msg="Collecting pickle from specified URL")
            with requests.get(path) as response:
                response.raise_for_status()
                model = pickle.loads(response.content)
                return model

        log.debug(msg="Collecting model pickle from local filesystem")
        with open(path, "rb") as f:
            model = pickle.load(f)
            log.debug(msg="Artifact loaded")
            return model
    except (
        FileNotFoundError,
        pickle.UnpicklingError,
        requests.HTTPError,
        TypeError,
        ModuleNotFoundError,
        Exception,
    ) as e:
        log.error(msg="Failed to load model artifact")
        log.error(msg=f"{type(e)}")
        log.error(msg=f"{e}")


def validate_artifact(artifact: Any) -> bool:
    if not isinstance(artifact, Pipeline):
        log.warning(msg="The model should be a Pipeline instance")
        log.warning(msg=f"Got {type(artifact)}")
        return False
    return True


def make_prediction(
    features: Union[List, pd.DataFrame]
) -> Optional[np.ndarray]:
    log.debug(msg="Predicts")
    if isinstance(features, list):
        log.debug(msg="Casting list to DataFrame")
        features = pd.DataFrame(features)
    try:
        return current_app.config["ARTIFACT"].predict(features)
    except Exception as e:
        log.error(msg="Prediction aborted")
        log.error(msg=f"{type(e)}")
        log.error(msg=f"{e}")
