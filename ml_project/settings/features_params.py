from dataclasses import dataclass, field
from typing import List, Optional
from . import DEFAULT_COLUMN_NAMES


@dataclass
class FeaturesConfig:
    target: str
    PCA_components: Optional[int] = None
    PCA_kernel: Optional[str] = field(default="linear")
    features_to_drop: List[str] = field(default_factory=lambda: [])
    categorical_features: List[str] = field(default_factory=lambda: [])
    numeric_features: List[str] = field(
        default_factory=lambda: DEFAULT_COLUMN_NAMES
    )
    numeric_imputer_strategy: str = field(default="mean")
    random_state: int = field(default=42)
