"""CLI for portfolio backtesting."""

import hydra
from omegaconf import DictConfig
from pathlib import Path
import pandas as pd

from ..utils.logging import setup_logging, task
from ..utils.io import read_parquet, write_csv
from ..backtest.engine import walk_forward
from ..backtest.metrics import calculate_metrics
from ..optimize.markowitz import mean_variance_weights


@hydra.main(version_base=None, config_path="../../../configs", config_name="experiment_hclust")
def main(cfg: DictConfig) -> None:
    """Main entry point for backtesting."""
    logger = setup_logging(cfg.logging.level, cfg.logging.rich)

    # Load prices
    with task("Loading prices", logger):
        prices = read_parquet(Path(cfg.paths.processed) / "prices.parquet")

    # Define optimizer function
    def optimize_portfolio(mu: pd.Series, Sigma: pd.DataFrame) -> pd.Series:
        return mean_variance_weights(
            mu=mu,
            Sigma=Sigma,
            lb=cfg.constraints.weight_bounds[0],
            ub=cfg.constraints.weight_bounds[1],
            rf=cfg.risk_model.risk_free_rate,
            objective=cfg.objective,
        )

    # Run backtest
    with task("Running backtest", logger):
        results = walk_forward(
            prices=prices,
            optimize=optimize_portfolio,
            rebalance_freq=cfg.rebalance.freq,
            transaction_costs_bps=cfg.rebalance.costs_bps,
        )

        logger.info(f"Backtest results shape: {results.shape}")
        logger.info(f"Date range: {results.index[0]} to {results.index[-1]}")

    # Calculate metrics
    with task("Calculating performance metrics", logger):
        metrics = calculate_metrics(
            returns=results["returns"],
            equity=results["equity"],
            risk_free_rate=cfg.risk_model.risk_free_rate,
        )

        logger.info("Performance Metrics:")
        for key, value in metrics.items():
            logger.info(f"  {key}: {value:.4f}")

    # Save results
    with task("Saving results", logger):
        Path(cfg.paths.artifacts).mkdir(parents=True, exist_ok=True)
        write_csv(results, Path(cfg.paths.artifacts) / "equity_curve.csv")
        metrics_df = pd.DataFrame([metrics])
        write_csv(metrics_df, Path(cfg.paths.artifacts) / "metrics.csv")

        logger.info(f"Results saved to {cfg.paths.artifacts}")


if __name__ == "__main__":
    main()
