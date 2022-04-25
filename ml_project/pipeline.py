import logging
from os import getenv, getcwd

from settings.root_params import RootConfig, resolve_cfg
from data import read_dataset, create_dataset

from features.extract import extract_target, extract_feature_columns

from features.process import (
    numeric_features_transform,
    categorial_features_transform,
    preprocessing_pipeline,
)

import hydra
from omegaconf import OmegaConf


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


@hydra.main(config_path="./configs", config_name="config")
def main(cfg: OmegaConf):
    log.info(msg="Training pipeline starting")
    log.debug(msg=f"Original working dir: {hydra.utils.get_original_cwd()}")
    log.debug(msg=f"Actual CWD: {getcwd()}")

    root_cfg = RootConfig(**OmegaConf.to_container(cfg, resolve=True))
    resolve_cfg(root_cfg)

    # log.debug(msg=f"Loaded config:{root_cfg}")

    data_cfg = root_cfg.data_params
    # split_cfg = root_cfg.split_params
    feature_cfg = root_cfg.feature_params
    # train_cfg = root_cfg.training_params

    log.debug(msg=f"Config Type: {type(data_cfg)}")

    create_dataset(
        data_cfg.source_url, data_cfg.dataset_dir, data_cfg.dataset_filename
    )

    raw_data = read_dataset(
        f"{data_cfg.dataset_dir}/{data_cfg.dataset_filename}",
        data_cfg.column_names,
        header=None,
    )

    log.debug(msg=f"Loaded dataset: {raw_data.shape}")
    log.debug(msg=f"Dataset columns: {raw_data.columns}")

    feature_columns = (
        feature_cfg.numeric_features + feature_cfg.categorical_features
    )

    target = extract_target(raw_data, feature_cfg.target)
    features = extract_feature_columns(raw_data, feature_columns)

    log.debug(msg=f"Feature columns: {feature_columns}")
    log.debug(msg=f"Target column: {target.shape}")

    num_transformer = numeric_features_transform(
        feature_cfg.scaler_type,
        feature_cfg.PCA_components,
        feature_cfg.PCA_kernel,
    )

    cat_transformer = categorial_features_transform(feature_cfg.encoder_type)

    preprocessor = preprocessing_pipeline(
        feature_cfg.categorical_features,
        feature_cfg.numeric_features,
        feature_cfg.numeric_imputer_strategy,
        num_transformer=num_transformer,
        cat_transformer=cat_transformer,
    )

    log.info(msg=f"Built preprocessor: \n{preprocessor}")
    processed_features = preprocessor.fit_transform(features)

    log.debug(msg=f"Processed: {processed_features.shape}")


if __name__ == "__main__":
    main()
