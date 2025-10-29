"""CLI for building features from prices."""

import hydra
from omegaconf import DictConfig
from pathlib import Path
import pandas as pd

from ..utils.logging import setup_logging, task
from ..utils.io import read_parquet, write_parquet
from ..features.returns import make_returns
from ..features.risk import ann_cov, shrink_cov
from ..features.corr import distance_from_corr


@hydra.main(version_base=None, config_path="../../../configs", config_name="experiment_hclust")
def main(cfg: DictConfig) -> None:
    """Main entry point for feature building."""
    logger = setup_logging(cfg.logging.level, cfg.logging.rich)

    # Load prices
    prices_path = Path(cfg.paths.processed) / "prices.parquet"
    with task("Loading prices", logger):
        prices = read_parquet(prices_path)

    # Calculate returns
    with task("Calculating returns", logger):
        returns = make_returns(
            prices,
            kind=cfg.returns.kind,
            window=cfg.returns.window,
        )
        write_parquet(returns, Path(cfg.paths.processed) / "returns.parquet")
        logger.info(f"Returns shape: {returns.shape}")

    # Calculate covariance matrix
    with task("Calculating covariance matrix", logger):
        cov = ann_cov(returns, ann_factor=cfg.risk.ann_factor)

        # Apply shrinkage if specified
        if cfg.corr.shrinkage != "none":
            cov = shrink_cov(cov, method=cfg.corr.shrinkage)

        write_parquet(cov, Path(cfg.paths.processed) / "covariance.parquet")
        logger.info(f"Covariance shape: {cov.shape}")

    # Calculate correlation and distance matrices
    with task("Calculating correlation and distance matrices", logger):
        corr = returns.corr(method=cfg.corr.method)
        distance = distance_from_corr(corr)

        write_parquet(corr, Path(cfg.paths.processed) / "correlation.parquet")
        write_parquet(distance, Path(cfg.paths.processed) / "distance.parquet")
        logger.info(f"Correlation shape: {corr.shape}")
        logger.info(f"Distance shape: {distance.shape}")


if __name__ == "__main__":
    main()
