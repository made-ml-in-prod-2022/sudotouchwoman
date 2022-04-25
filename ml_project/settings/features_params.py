from dataclasses import dataclass, field
from typing import List, Optional
from . import FEATURES


@dataclass
class FeaturesConfig:
    target: str
    PCA_components: Optional[int] = None
    PCA_kernel: Optional[str] = field(default="linear")
    scaler_type: str = field(default="StandardScaler")
    encoder_type: str = field(default="OneHotEncoder")
    features_to_drop: List[str] = field(default_factory=lambda: [])
    categorical_features: List[str] = field(default_factory=lambda: [])
    numeric_features: List[str] = field(
        default_factory=lambda: list(FEATURES)
    )
    numeric_imputer_strategy: str = field(default="mean")
    random_state: int = field(default=42)
