from dataclasses import dataclass

from .data_params import DatasetConfig, SplitConfig
from .features_params import FeaturesConfig
from .training_params import EstimatorConfig


@dataclass
class RootConfig:
    dir_prefix: str
    dataset: DatasetConfig
    feature: FeaturesConfig
    estimator: EstimatorConfig
    splitter: SplitConfig
    random_state: int


def resolve_cfg(cfg: RootConfig) -> None:
    cfg.dataset = DatasetConfig(**cfg.dataset)
    cfg.feature = FeaturesConfig(**cfg.feature)
    cfg.estimator = EstimatorConfig(**cfg.estimator)
    cfg.splitter = SplitConfig(**cfg.splitter)


@dataclass
class InfConfig:
    artifact: str
    input_features: str
    output_target: str
