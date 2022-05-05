from dataclasses import dataclass, field
from typing import List, Optional
from . import DEFAULT_COLUMN_NAMES


@dataclass
class DatasetConfig:
    source_url: str
    dataset_dir: str
    dataset_filename: str
    download: bool = False
    column_names: List[str] = field(
        default_factory=lambda: DEFAULT_COLUMN_NAMES
    )
    random_state: int = 42
    header: Optional[int] = None


@dataclass
class SplitConfig:
    validation: float
    random_state: int = 42
