import logging
from os import getenv
from typing import List

from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.decomposition import KernelPCA
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer, make_column_transformer


__all__ = [
    "numeric_features_transform",
    "categorial_features_transform",
    "preprocessing_pipeline",
]


def _make_logger(name: str) -> logging.Logger:

    log = logging.getLogger(name)

    if not log.hasHandlers():
        DEBUGLEVEL = getenv("DEBUG_LEVEL", "DEBUG")
        log.disabled = getenv("WRITE_LOGS", "True") == "False"

        log.setLevel(getattr(logging, DEBUGLEVEL))

        logging.basicConfig(
            format="[%(asctime)s]::[%(name)s]::[%(levelname)s]::%(message)s",
            datefmt="%D # %H:%M:%S",
        )

    return log


log = _make_logger(__name__)


def numeric_features_transform(
    scaler_type: str,
    principal_components: int = None,
    pca_kernel: str = "linear",
) -> Pipeline:
    """
    Creates pipeline for numerical features:
    use specified scaler and PCA, if required

    :param scaler: scaler type: standard or robust
    :param principal_components: int or None,
    if not None, add PCA layer after scaling with specified kernel
    :param pca_kernel: PCA kernel to use. Default is a linear kernel

    :rtype : Pipeline
    """
    scalers = dict(standard=StandardScaler, robust=RobustScaler)
    if scaler_type not in scalers.keys():
        error_message = (
            f"Invalid scaler: {scaler_type}. Expected {scalers.keys()}"
        )
        log.error(msg=error_message)
        raise ValueError(error_message)

    # log.debug(msg=f"Creates pipeline for numeric features using\
    #     PCA-{principal_components} and {pca_kernel} kernel")
    log.debug(msg="Adding scaler to numeric pipeline")
    selected_scaler = scalers[scaler_type]
    # data = selected_scaler.fit_transform(data)
    steps = [selected_scaler()]

    if principal_components:
        log.debug(msg="Adding PCA layer to numeric pipeline")
        pca = KernelPCA(n_components=principal_components, kernel=pca_kernel)
        steps += [pca]

    return make_pipeline(*steps)


def categorial_features_transform(encoder_type: str) -> Pipeline:
    """
    Creates pipeline for categorical features:
    essentially encodes them using
    one-hot/ordinal encoding

    :param encoder_type, str: encoder type. Ensemble models
    conventionally require ordinal encoding while
    liner/NB/SVM models need one-hot encoded features

    :rtype : Pipeline
    """
    encoders = dict(ohe=OneHotEncoder, ordinal=OrdinalEncoder)
    encoder_params = dict(categories="auto", handle_unknown="ignore")

    if encoder_type not in encoders.keys():
        error_message = (
            f"Invalid encoder: {encoder_type}. Expected {encoders.keys()}"
        )
        log.error(msg=error_message)
        raise ValueError(error_message)

    log.debug(msg="Adding encoder to categorical pipeline")
    steps = []
    encoder = encoders[encoder_type](**encoder_params)
    # encoder.fit(data)
    steps += [encoder]

    return make_pipeline(*steps)


def preprocessing_pipeline(
    cat_features: List[str],
    num_features: List[str],
    num_imputer_strategy: str,
    num_transformer: Pipeline,
    cat_transformer: Pipeline,
) -> ColumnTransformer:
    log.debug(msg="Creating imputer for missing values")
    num_imputer = SimpleImputer(strategy=num_imputer_strategy)
    cat_imputer = SimpleImputer(strategy="most_frequent")

    return make_column_transformer(
        (make_pipeline(num_imputer, num_transformer), num_features),
        (make_pipeline(cat_imputer, cat_transformer), cat_features),
    )
