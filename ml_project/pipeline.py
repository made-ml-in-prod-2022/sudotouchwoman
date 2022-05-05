import logging
from os import getcwd

import hydra
from hydra.utils import instantiate
from omegaconf import OmegaConf

from settings.root_params import RootConfig
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


@hydra.main(config_path="./configs", config_name="training")
def main(cfg: OmegaConf):
    log.info(msg="Training pipeline starting")
    log.debug(msg=f"Original working dir: {hydra.utils.get_original_cwd()}")
    log.debug(msg=f"Actual CWD: {getcwd()}")

    root_cfg: RootConfig = instantiate(cfg)

    dataset = root_cfg.dataset
    splitter = root_cfg.splitter
    feature = root_cfg.feature
    estimator = root_cfg.estimator

    create_dataset(dataset)
    raw_data = read_dataset(dataset)
    log.info(msg=f"Loaded dataset: {raw_data.shape}")
    log.debug(msg=f"Dataset columns: {raw_data.columns.to_list()}")

    feature_columns = (
        feature.numeric_features + feature.categorical_features
    )

    target = extract_target(raw_data, feature.target)
    features = extract_feature_columns(raw_data, feature_columns)

    log.info(msg="Splitting the dataset")
    train_features, val_features, train_y, val_y = split_data(
        features, target, splitter
    )
    log.debug(msg=f"Train set: {train_features.shape}: {train_y.shape}")
    log.debug(msg=f"Val set: {val_features.shape}: {val_y.shape}")

    num_transformer = numeric_features_transform(
        feature.scaler_type,
        feature.PCA_components,
        feature.PCA_kernel,
    )

    cat_transformer = categorical_features_transform(feature.encoder_type)

    preprocessor = preprocessing_pipeline(
        feature.categorical_features,
        feature.numeric_features,
        feature.numeric_imputer_strategy,
        num_transformer=num_transformer,
        cat_transformer=cat_transformer,
    )

    log.info(msg="Built preprocessor")
    log.debug(msg=f"\n{preprocessor}")

    train_features_processed = preprocessor.fit_transform(train_features)

    end_to_end_pipeline = make_inference_pipeline(
        preprocessor,
        make_estimator(train_features_processed, train_y, estimator),
    )
    log.info(msg="Created end-to-end inference pipeline")

    metrics = get_metrics(
        val_y,
        end_to_end_pipeline.predict(val_features),
        estimator
    )
    log.info(msg=f"Collected metrics: {metrics}")
    metrics.dump(estimator.metrics_path)

    log.info(msg=f"Dumps artifact to {estimator.model_artifact_path}")
    dump_pipeline(end_to_end_pipeline, estimator.model_artifact_path)

    log.info(msg="Training pipeline finished")


if __name__ == "__main__":
    main()
