from itertools import chain

FEATURE_TYPES = (
    "radius",
    "texture",
    "peri",
    "area",
    "smoothness",
    "compactness",
    "concavity",
    "concave_points",
    "symmetry",
    "fractal_dim",
)

FEATURES = chain(
    map(lambda x: f"{x}_mean", FEATURE_TYPES),
    map(lambda x: f"{x}_se", FEATURE_TYPES),
    map(lambda x: f"{x}_worst", FEATURE_TYPES),
)

FEATURES = tuple(FEATURES)
DEFAULT_COLUMN_NAMES = ["id", "diag", *FEATURES]
