from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class EstimatorConfig:
    model_type: str
    model_params: Dict[str, Any]
    random_state: int = field(default=42)
