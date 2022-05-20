import logging
import numpy as np

import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from settings.features_params import FeaturesConfig

from .process import (
    numeric_features_transform,
    categorical_features_transform,
    preprocessing_pipeline,
)


log = logging.getLogger(__name__)


class Preprocessor(BaseEstimator, TransformerMixin):
    def __init__(self, cfg: FeaturesConfig) -> None:
        log.debug(msg="Instantiating preprocessor")
        self.cfg = cfg

        self.transformer = self._build_column_transformer(
            num_transform=self._build_numeric_pipeline(),
            cat_transform=self._build_categorical_pipeline(),
        )

    def fit(self, X: pd.DataFrame, y=None) -> "Preprocessor":
        log.debug(msg="Fitting preprocessor")
        x = X.drop(columns=self.cfg.features_to_drop)
        self.transformer.fit(X=x)
        return self

    def transform(self, X: pd.DataFrame, y=None) -> np.ndarray:
        log.debug(msg="Transforming features")
        x = X.drop(columns=self.cfg.features_to_drop)
        return self.transformer.transform(X=x)

    def __repr__(self, N_CHAR_MAX: int = 700) -> str:
        return "Preprocessor: " + self.transformer.__repr__(N_CHAR_MAX)

    def _build_numeric_pipeline(self) -> Pipeline:
        return numeric_features_transform(
            scaler_type=self.cfg.scaler_type,
            principal_components=self.cfg.PCA_components,
            pca_kernel=self.cfg.PCA_kernel,
        )

    def _build_categorical_pipeline(self) -> Pipeline:
        return categorical_features_transform(
            encoder_type=self.cfg.encoder_type
        )

    def _build_column_transformer(
        self, num_transform: Pipeline, cat_transform: Pipeline
    ) -> ColumnTransformer:
        return preprocessing_pipeline(
            self.cfg.categorical_features,
            self.cfg.numeric_features,
            self.cfg.numeric_imputer_strategy,
            num_transform,
            cat_transform,
        )
