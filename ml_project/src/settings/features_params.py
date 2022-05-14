from dataclasses import dataclass, field
from typing import List, Optional
from . import FEATURES


@dataclass
class FeaturesConfig:
    target: str
    PCA_components: Optional[int] = None
    PCA_kernel: Optional[str] = "linear"
    scaler_type: str = "standard"
    encoder_type: str = "ohe"
    features_to_drop: List[str] = field(default_factory=lambda: [])
    categorical_features: List[str] = field(default_factory=lambda: [])
    numeric_features: List[str] = field(default_factory=lambda: list(FEATURES))
    numeric_imputer_strategy: str = "mean"
    random_state: int = 42
