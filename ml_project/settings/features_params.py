from dataclasses import dataclass, field
from typing import List, Optional
from . import DEFAULT_COLUMN_NAMES


@dataclass
class FeaturesConfig:
    target: str
    std: Optional[float]
    mean: Optional[float]
    PCA_components: Optional[int]
    features_to_drop: List[str] = []
    categorical_features: List[str] = []
    numeric_features: List[str] = DEFAULT_COLUMN_NAMES
    random_state: int = field(default=42)
