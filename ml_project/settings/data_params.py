from dataclasses import dataclass, field
from typing import List, Union
from . import DEFAULT_COLUMN_NAMES


@dataclass
class DatasetConfig:
    source_url: str
    dataset_dir: str
    dataset_filename: str
    column_names: List[str] = DEFAULT_COLUMN_NAMES
    header: int = field(default=None)
    random_state: int = field(default=42)


@dataclass
class SplitConfig:
    validation: Union[int, float]
    random_state: int = field(default=42)