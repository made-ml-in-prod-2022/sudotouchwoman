import pickle
from typing import Optional

from sklearn.pipeline import Pipeline

from .. import default_logger

log = default_logger(__name__)


def load_artifact(path: str) -> Optional[Pipeline]:
    log.debug(msg=f"Reading model artifact from {path}")
    try:
        with open(path, "rb") as f:
            model = pickle.load(f)
            log.debug(msg="Artifact loaded")
            return model
    except (
        FileNotFoundError,
        pickle.UnpicklingError,
        TypeError,
        ModuleNotFoundError,
    ) as e:
        log.error(msg="Failed to load model artifact")
        log.error(msg=f"{e}")
        return
