import logging
from os import getcwd

import hydra
from omegaconf import OmegaConf

from settings.root_params import RootConfig, resolve_cfg
from data import read_dataset, create_dataset

from features.extract import (
    extract_target,
    extract_feature_columns,
    split_data,
)
from features.process import (
    numeric_features_transform,
    categorical_features_transform,
    preprocessing_pipeline,
)
from models import (
    make_estimator,
    make_inference_pipeline,
    get_metrics,
    dump_pipeline,
)


log = logging.getLogger(__name__)


@hydra.main(config_path="./configs", config_name="config")
def main(cfg: OmegaConf):
    log.info(msg="Training pipeline starting")
    log.debug(msg=f"Original working dir: {hydra.utils.get_original_cwd()}")
    log.debug(msg=f"Actual CWD: {getcwd()}")

    root_cfg = RootConfig(**OmegaConf.to_container(cfg, resolve=True))
    # unpack nested dataclasses for dot-notation access,
    # like root_cfg.data_params.source_url
    # otherwise these would be dicts
    resolve_cfg(root_cfg)

    data_cfg = root_cfg.dataset
    split_cfg = root_cfg.splitter
    feature_cfg = root_cfg.feature
    train_cfg = root_cfg.estimator

    create_dataset(data_cfg)
    raw_data = read_dataset(data_cfg)
    log.debug(msg=f"Loaded dataset: {raw_data.shape}")
    log.debug(msg=f"Dataset columns: {raw_data.columns}")

    feature_columns = (
        feature_cfg.numeric_features + feature_cfg.categorical_features
    )

    target = extract_target(raw_data, feature_cfg.target)
    features = extract_feature_columns(raw_data, feature_columns)
    log.debug(msg=f"Feature columns: {feature_columns}")
    log.debug(msg=f"Target column: {target.shape}")

    log.info(msg="Splitting the dataset")
    train_features, val_features, train_y, val_y = split_data(
        features, target, split_cfg
    )
    log.debug(msg=f"Train set: {train_features.shape}: {train_y.shape}")
    log.debug(msg=f"Val set: {val_features.shape}: {val_y.shape}")

    num_transformer = numeric_features_transform(
        feature_cfg.scaler_type,
        feature_cfg.PCA_components,
        feature_cfg.PCA_kernel,
    )

    cat_transformer = categorical_features_transform(feature_cfg.encoder_type)

    preprocessor = preprocessing_pipeline(
        feature_cfg.categorical_features,
        feature_cfg.numeric_features,
        feature_cfg.numeric_imputer_strategy,
        num_transformer=num_transformer,
        cat_transformer=cat_transformer,
    )

    log.info(msg="Built preprocessor")
    log.debug(msg=f"\n{preprocessor}")

    train_features_processed = preprocessor.fit_transform(train_features)
    log.debug(msg=f"Processed: {train_features_processed.shape}")

    end_to_end_pipeline = make_inference_pipeline(
        preprocessor,
        make_estimator(train_features_processed, train_y, train_cfg),
    )
    log.info(msg="Created end-to-end inference pipeline")

    metrics = get_metrics(
        val_y,
        end_to_end_pipeline.predict(val_features),
        train_cfg
    )
    log.info(msg=f"{metrics}")

    log.info(msg=f"Dumps artifact to {train_cfg.model_artifact_path}")
    dump_pipeline(end_to_end_pipeline, train_cfg.model_artifact_path)
    log.info(msg="Training pipeline finished")


if __name__ == "__main__":
    main()
