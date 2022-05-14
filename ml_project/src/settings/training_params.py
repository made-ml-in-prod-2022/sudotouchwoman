from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class EstimatorConfig:
    model_type: str
    pos_label: str
    neg_label: str
    model_artifact_path: str
    metrics_path: str
    model_params: Dict[str, Any]
    random_state: int = field(default=42)
