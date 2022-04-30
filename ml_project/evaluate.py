import logging

import hydra
from omegaconf import OmegaConf

# from models import load_pipeline

log = logging.getLogger(__name__)


@hydra.main(config_path="./configs", config_name="inference")
def main(cfg: OmegaConf) -> None:
    return


if __name__ == "__main__":
    pass
