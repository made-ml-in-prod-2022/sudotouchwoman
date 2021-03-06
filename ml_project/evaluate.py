import logging
from os import getcwd

import hydra
from hydra.utils import instantiate
from omegaconf import OmegaConf

from src.models import load_pipeline, dump_prediction
from src.data import read_inference_data


log = logging.getLogger(__name__)


@hydra.main(config_path="./configs", config_name="inference")
def main(cfg: OmegaConf) -> None:
    log.info(msg="Inference pipeline starting")
    log.debug(msg=f"Original working dir: {hydra.utils.get_original_cwd()}")
    log.debug(msg=f"Actual CWD: {getcwd()}")

    inf_config = instantiate(cfg.inference)
    pipeline = load_pipeline(inf_config.artifact)
    log.info(msg=f"Loaded pipeline: {pipeline}")

    features = read_inference_data(inf_config.input_features)
    prediction = pipeline.predict(features)
    dump_prediction(prediction, inf_config.output_target)

    log.info(msg="Inference pipeline finished")


if __name__ == "__main__":
    main()
