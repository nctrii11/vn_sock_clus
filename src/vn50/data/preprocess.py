"""Data preprocessing utilities."""

import pandas as pd


def align_calendar(prices: pd.DataFrame) -> pd.DataFrame:
    """Align calendar dates across all tickers.

    Removes dates where any ticker has NaN value and sorts by date.

    Args:
        prices: Wide DataFrame (index=Date, columns=tickers)

    Returns:
        DataFrame with aligned calendar (no NaNs, sorted by date)
    """
    # Forward fill and backward fill to handle non-trading days
    prices = prices.ffill().bfill()

    # Drop rows where any value is still NaN
    prices = prices.dropna()

    # Sort by date
    prices = prices.sort_index()

    # Remove duplicate dates
    prices = prices[~prices.index.duplicated(keep="first")]

    return prices


def fill_missing(prices: pd.DataFrame, method: str = "ffill") -> pd.DataFrame:
    """Fill missing values in price data.

    Args:
        prices: Wide DataFrame
        method: Method for filling ('ffill', 'bfill', 'interpolate')

    Returns:
        DataFrame with filled values
    """
    if method == "ffill":
        return prices.ffill().bfill()
    elif method == "bfill":
        return prices.bfill().ffill()
    elif method == "interpolate":
        return prices.interpolate(method="linear")
    else:
        raise ValueError(f"Unknown fill method: {method}")
