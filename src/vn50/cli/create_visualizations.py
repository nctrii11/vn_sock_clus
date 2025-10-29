"""CLI for creating visualizations."""

import hydra
from omegaconf import DictConfig
from pathlib import Path

from ..utils.logging import setup_logging, task
from ..visualization import create_all_visualizations


@hydra.main(version_base=None, config_path="../../../configs", config_name="experiment_hclust")
def main(cfg: DictConfig) -> None:
    """Main entry point for visualization generation."""
    logger = setup_logging(cfg.logging.level, cfg.logging.rich)

    with task("Creating visualizations", logger):
        create_all_visualizations(
            data_dir=cfg.paths.processed,
            output_dir=f"{cfg.paths.reports}/figures"
        )
        logger.info("All visualizations created successfully!")


if __name__ == "__main__":
    main()
