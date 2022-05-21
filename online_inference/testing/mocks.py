import json
import pickle
from typing import Dict

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler


def testing_artifact(filename: str) -> str:
    pipe = make_pipeline(RobustScaler())
    with open(filename, "wb+") as f:
        pickle.dump(pipe, f)
    return filename


def testing_stats(filename: str) -> str:
    stats = {"mean": [0], "std": [1]}
    with open(filename, "w+") as f:
        json.dump(stats, f)
    return filename


def testing_schema(filename: str, schema: Dict[str, str]) -> str:
    with open(filename, "w+") as f:
        json.dump(schema, f)
    return filename
