"""CLI for portfolio optimization."""

import hydra
from omegaconf import DictConfig
from pathlib import Path
import pandas as pd

from ..utils.logging import setup_logging, task
from ..utils.io import read_parquet, write_parquet
from ..optimize.markowitz import mean_variance_weights


@hydra.main(version_base=None, config_path="../../../configs", config_name="experiment_hclust")
def main(cfg: DictConfig) -> None:
    """Main entry point for portfolio optimization."""
    logger = setup_logging(cfg.logging.level, cfg.logging.rich)

    # Load data
    with task("Loading data", logger):
        returns = read_parquet(Path(cfg.paths.processed) / "returns.parquet")
        cov = read_parquet(Path(cfg.paths.processed) / "covariance.parquet")

    # Calculate expected returns
    with task("Calculating expected returns", logger):
        mu = returns.mean() * 252  # Annualized

    # Optimize portfolio
    with task("Optimizing portfolio", logger):
        weights = mean_variance_weights(
            mu=mu,
            Sigma=cov,
            lb=cfg.constraints.weight_bounds[0],
            ub=cfg.constraints.weight_bounds[1],
            rf=cfg.risk_model.risk_free_rate,
            objective=cfg.objective,
        )

        logger.info(f"Number of assets in portfolio: {(weights > 0).sum()}")
        logger.info(f"Weight sum: {weights.sum():.4f}")
        logger.info(f"Min weight: {weights.min():.4f}")
        logger.info(f"Max weight: {weights.max():.4f}")

    # Save weights
    with task("Saving portfolio weights", logger):
        Path(cfg.paths.artifacts).mkdir(parents=True, exist_ok=True)
        output_path = Path(cfg.paths.artifacts) / "initial_weights.parquet"
        write_parquet(weights.to_frame(name="weight"), output_path)

        # Also save as CSV for readability
        weights.to_csv(Path(cfg.paths.artifacts) / "initial_weights.csv")

        logger.info(f"Top 5 holdings: {weights.nlargest(5).to_dict()}")


if __name__ == "__main__":
    main()
