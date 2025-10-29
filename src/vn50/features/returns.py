"""Return calculation utilities."""

import numpy as np
import pandas as pd


def make_returns(
    prices: pd.DataFrame,
    kind: str = "log",
    window: int = 1,
) -> pd.DataFrame:
    """Calculate returns from prices.

    Pure function: no I/O, returns DataFrame with same columns as input.

    Args:
        prices: Wide DataFrame (index=Date, columns=tickers)
        kind: Type of returns ('log' or 'arith')
        window: Rolling window size (default: 1 for daily returns)

    Returns:
        Returns DataFrame with same shape as input (excluding first row)
    """
    if kind == "log":
        rets = prices.pct_change(periods=window)
        rets = rets.apply(lambda x: np.log1p(x))
    elif kind == "arith":
        rets = prices.pct_change(periods=window)
    else:
        raise ValueError(f"Unknown return kind: {kind}. Must be 'log' or 'arith'")

    # Drop first row(s) with NaN
    rets = rets.dropna(how="all")

    return rets


def cumulative_returns(returns: pd.DataFrame) -> pd.DataFrame:
    """Calculate cumulative returns.

    Args:
        returns: Returns DataFrame

    Returns:
        Cumulative returns DataFrame
    """
    return (1 + returns).cumprod()


def annualized_returns(returns: pd.DataFrame, periods_per_year: int = 252) -> pd.Series:
    """Calculate annualized returns.

    Args:
        returns: Returns DataFrame
        periods_per_year: Number of periods per year (default: 252 for daily)

    Returns:
        Annualized returns Series
    """
    total_return = (1 + returns).prod() - 1
    n_periods = len(returns)
    years = n_periods / periods_per_year
    ann_ret = (1 + total_return) ** (1 / years) - 1
    return ann_ret
