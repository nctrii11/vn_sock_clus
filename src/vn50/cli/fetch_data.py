"""CLI for fetching market data."""

import hydra
from omegaconf import DictConfig
from pathlib import Path

from ..utils.logging import setup_logging, task
from ..data.fetch import load_or_fetch


@hydra.main(version_base=None, config_path="../../../configs", config_name="experiment_hclust")
def main(cfg: DictConfig) -> None:
    """Main entry point for data fetching."""
    logger = setup_logging(cfg.logging.level, cfg.logging.rich)

    with task("Load or fetch prices", logger):
        # Get symbols from config (data.yaml is merged at root level)
        symbols = cfg.symbols.custom if cfg.symbols.custom else cfg.symbols.vn30

        # Add .VN suffix for yfinance
        symbols_vn = [f"{s}.VN" for s in symbols]

        # Resolve OmegaConf interpolations
        start_date = str(cfg.calendar.start)
        end_date = str(cfg.calendar.end)

        # If end_date contains unresolved interpolation, use today's date
        if "YYYY-MM-DD" in end_date or end_date.startswith("${"):
            from datetime import datetime

            end_date = datetime.now().strftime("%Y-%m-%d")

        # Load or fetch data
        prices = load_or_fetch(
            cache_dir=Path(cfg.paths.cache),
            symbols=symbols_vn,
            start=start_date,
            end=end_date,
            adjust=cfg.price.adjust,
        )

        logger.info(f"Fetched data for {len(prices.columns)} symbols")
        logger.info(f"Date range: {prices.index[0]} to {prices.index[-1]}")
        logger.info(f"Data shape: {prices.shape}")

        # Save to processed
        output_path = Path(cfg.paths.processed) / "prices.parquet"
        from ..utils.io import write_parquet

        Path(cfg.paths.processed).mkdir(parents=True, exist_ok=True)
        write_parquet(prices, output_path)
        logger.info(f"Saved prices to {output_path}")


if __name__ == "__main__":
    main()
