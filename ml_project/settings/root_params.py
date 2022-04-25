from dataclasses import dataclass

from .data_params import DatasetConfig, SplitConfig
from .features_params import FeaturesConfig
from .training_params import EstimatorConfig


@dataclass
class RootConfig:
    data_params: DatasetConfig
    feature_params: FeaturesConfig
    training_params: EstimatorConfig
    split_params: SplitConfig
    metrics_path: str
    model_artifact_path: str


def resolve_cfg(cfg: RootConfig) -> None:
    cfg.data_params = DatasetConfig(**cfg.data_params)
    cfg.feature_params = FeaturesConfig(**cfg.feature_params)
    cfg.training_params = EstimatorConfig(**cfg.training_params)
    cfg.split_params = SplitConfig(**cfg.split_params)
