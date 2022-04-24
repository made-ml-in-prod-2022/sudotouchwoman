from itertools import chain

from .data_params import DatasetConfig, SplitConfig
from .features_params import FeaturesConfig
from .training_params import EstimatorConfig
from .root_params import RootConfig


__all__ = [
    "DatasetConfig",
    "SplitConfig",
    "FeaturesConfig",
    "EstimatorConfig",
    "RootConfig",
]

FEATURE_TYPES = (
    "radius",
    "texture",
    "peri",
    "area",
    "smoothness",
    "compactness",
    "concavity",
    "concave_points",
    "symmetry",
    "fractal_dim",
)

FEATURES = chain(
    map(lambda x: f"{x}_mean", FEATURE_TYPES),
    map(lambda x: f"{x}_se", FEATURE_TYPES),
    map(lambda x: f"{x}_worst", FEATURE_TYPES),
)

DEFAULT_COLUMN_NAMES = ["id", "diag", *FEATURES]
