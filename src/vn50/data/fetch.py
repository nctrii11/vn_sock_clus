"""Data fetching utilities for VN market using vnstock."""

from __future__ import annotations

from pathlib import Path
import time

import pandas as pd
from vnstock import stock_historical_data

from ..utils.io import read_parquet, write_parquet
from .preprocess import align_calendar


def fetch_prices(symbols: list[str], start: str, end: str, adjust: bool = True) -> pd.DataFrame:
    """Fetch historical prices for VN market symbols using vnstock.

    Fetches data from vnstock (cafe.vn) and returns a wide DataFrame with:
    - Index: DatetimeIndex (sorted ascending)
    - Columns: Ticker symbols
    - Values: Close prices

    Args:
        symbols: List of ticker symbols (e.g., ["VCB", "VIC"])
        start: Start date (YYYY-MM-DD)
        end: End date (YYYY-MM-DD)
        adjust: Whether to use adjusted prices (default: True, not used in vnstock)

    Returns:
        Wide DataFrame with Date index and tickers as columns (Close prices)

    Raises:
        ValueError: If symbols list is empty or no data available
    """
    if not symbols:
        raise ValueError("Symbols list cannot be empty")

    # Fetch data for each symbol
    all_prices = {}
    for symbol in symbols:
        try:
            # Remove .VN suffix if present
            symbol_clean = symbol.replace('.VN', '')
            
            # Get historical data using vnstock
            df = stock_historical_data(
                symbol=symbol_clean,
                start_date=start,
                end_date=end,
                resolution='1D',
                type='stock'
            )
            
            if df is not None and not df.empty and 'close' in df.columns:
                # Set index to time/date column
                if 'time' in df.columns:
                    df['time'] = pd.to_datetime(df['time'])
                    df = df.set_index('time')
                elif 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'])
                    df = df.set_index('date')
                
                # Remove duplicates
                df = df[~df.index.duplicated(keep='first')]
                all_prices[symbol] = df['close']
            else:
                print(f"Warning: No data for {symbol}")
                
        except Exception as e:
            print(f"Warning: Error fetching {symbol}: {e}")
            continue
        
        # Sleep to avoid rate limiting
        time.sleep(0.3)

    if not all_prices:
        raise ValueError("No data available for any symbol")

    # Get union of all dates
    all_dates = pd.DatetimeIndex([])
    for symbol, series in all_prices.items():
        all_dates = all_dates.union(series.index)
    
    all_dates = all_dates.sort_values()
    
    # Create DataFrame with aligned dates
    prices = pd.DataFrame(index=all_dates)
    for symbol, series in all_prices.items():
        prices[symbol] = series
    
    # Sort by date
    prices = prices.sort_index()
    
    # Fill forward missing values
    prices = prices.ffill()

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
