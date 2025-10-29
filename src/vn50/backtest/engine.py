"""Backtesting engine for portfolio optimization."""

import pandas as pd
from typing import Callable


def walk_forward(
    prices: pd.DataFrame,
    optimize: Callable[[pd.Series, pd.DataFrame], pd.Series],
    rebalance_freq: str = "M",
    transaction_costs_bps: float = 10.0,
) -> pd.DataFrame:
    """Walk-forward backtesting engine.

    Args:
        prices: Prices DataFrame
        optimize: Optimization function that takes (mu, Sigma) and returns weights
        rebalance_freq: Rebalancing frequency ('D', 'W', 'M')
        transaction_costs_bps: Transaction costs in basis points

    Returns:
        DataFrame with dates as index and columns:
        - returns: Portfolio returns
        - equity: Cumulative equity curve
        - turnover: Portfolio turnover at each rebalance
    """
    # Calculate returns
    returns = prices.pct_change().dropna()

    # Group by rebalancing frequency
    results = []
    equity = 1.0
    prev_weights = None

    for date, group in returns.groupby(pd.Grouper(freq=rebalance_freq)):
        # Skip if no data
        if group.empty:
            continue

        # Calculate expected returns and covariance from historical data
        mu = group.mean() * 252  # Annualized
        Sigma = group.cov() * 252  # Annualized

        # Optimize portfolio
        weights = optimize(mu, Sigma)

        # Calculate portfolio return
        port_return = (group * weights).sum(axis=1)

        # Calculate turnover (if not first rebalance)
        turnover = 0.0
        if prev_weights is not None:
            turnover = (weights - prev_weights).abs().sum()

        # Update equity (apply transaction costs if turnover > 0)
        cost_multiplier = 1.0 - (transaction_costs_bps / 10000) * turnover
        equity_timeseries = equity * (1 + port_return).cumprod() * cost_multiplier
        equity = equity_timeseries.iloc[-1]

        prev_weights = weights.copy()

        # Store results
        results.append(
            {
                "date": date,
                "returns": port_return,
                "equity": equity_timeseries,
                "turnover": turnover,
                "weights": weights,
            }
        )

    # Combine results
    equity_curve = pd.concat([r["equity"] for r in results])
    returns_series = pd.concat([r["returns"] for r in results])
    turnover_series = pd.Series({r["date"]: r["turnover"] for r in results})

    # Return DataFrame
    result_df = pd.DataFrame(
        {
            "returns": returns_series,
            "equity": equity_curve,
        },
    )
    result_df.index.name = "date"

    return result_df


def run_backtest(
    prices: pd.DataFrame,
    start_date: str,
    end_date: str,
    optimize: Callable,
    rebalance_freq: str = "M",
    transaction_costs_bps: float = 10.0,
) -> dict:
    """Run backtest over specified date range.

    Args:
        prices: Prices DataFrame
        start_date: Start date for backtest
        end_date: End date for backtest
        optimize: Optimization function
        rebalance_freq: Rebalancing frequency
        transaction_costs_bps: Transaction costs in basis points

    Returns:
        Dictionary with backtest results
    """
    # Filter data to date range
    prices_filtered = prices.loc[start_date:end_date]

    # Run walk-forward backtest
    results = walk_forward(
        prices_filtered,
        optimize,
        rebalance_freq=rebalance_freq,
        transaction_costs_bps=transaction_costs_bps,
    )

    return results
