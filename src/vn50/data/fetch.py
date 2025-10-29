"""Data fetching utilities for VN market using yfinance."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import yfinance as yf

from ..utils.io import read_parquet, write_parquet
from .preprocess import align_calendar


def fetch_prices(symbols: list[str], start: str, end: str, adjust: bool = True) -> pd.DataFrame:
    """Fetch historical prices for VN market symbols.

    Fetches data from yfinance and returns a wide DataFrame with:
    - Index: DatetimeIndex (sorted ascending)
    - Columns: Ticker symbols
    - Values: Close prices (adjusted by default)

    Args:
        symbols: List of ticker symbols (e.g., ["VCB.VN", "VIC.VN"])
        start: Start date (YYYY-MM-DD)
        end: End date (YYYY-MM-DD)
        adjust: Whether to use adjusted prices (default: True)

    Returns:
        Wide DataFrame with Date index and tickers as columns (Close prices)

    Raises:
        ValueError: If symbols list is empty or no data available
    """
    if not symbols:
        raise ValueError("Symbols list cannot be empty")

    # Fetch data for each symbol
    dfs = []
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            df_ticker = ticker.history(start=start, end=end, auto_adjust=adjust)
            if df_ticker.empty:
                print(f"Warning: No data for {symbol}")
                continue
            dfs.append((symbol, df_ticker))
        except Exception as e:
            print(f"Warning: Error fetching {symbol}: {e}")
            continue

    if not dfs:
        raise ValueError("No data available for any symbol")

    # Combine into wide format
    prices_list = []
    for symbol, df in dfs:
        prices_list.append(df[["Close"]].rename(columns={"Close": symbol}))

    # Merge all tickers
    prices = pd.concat(prices_list, axis=1)

    # Sort by date
    prices = prices.sort_index()

    # Remove duplicate dates
    prices = prices[~prices.index.duplicated(keep="first")]

    return prices


def load_or_fetch(
    cache_dir: Path,
    symbols: list[str],
    start: str,
    end: str,
    adjust: bool = True,
) -> pd.DataFrame:
    """Load prices from cache or fetch from API.

    Args:
        cache_dir: Directory to cache data
        symbols: List of ticker symbols
        start: Start date
        end: End date
        adjust: Whether to use adjusted prices

    Returns:
        DataFrame with prices
    """
    cache_file = cache_dir / "prices.parquet"
    if cache_file.exists():
        return read_parquet(cache_file)

    prices = fetch_prices(symbols, start, end, adjust)
    prices = align_calendar(prices)

    cache_file.parent.mkdir(parents=True, exist_ok=True)
    write_parquet(prices, cache_file)

    return prices
