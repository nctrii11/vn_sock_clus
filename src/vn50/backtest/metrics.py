"""Performance metrics for portfolio backtesting."""

import numpy as np
import pandas as pd


def sharpe_ratio(
    returns: pd.Series, risk_free_rate: float = 0.02, periods_per_year: int = 252
) -> float:
    """Calculate Sharpe ratio.

    Args:
        returns: Returns Series
        risk_free_rate: Risk-free rate (annualized)
        periods_per_year: Number of periods per year

    Returns:
        Sharpe ratio
    """
    excess_returns = returns.mean() * periods_per_year - risk_free_rate
    volatility = returns.std() * np.sqrt(periods_per_year)
    if volatility == 0:
        return 0.0
    return excess_returns / volatility


def sortino_ratio(
    returns: pd.Series, risk_free_rate: float = 0.02, periods_per_year: int = 252
) -> float:
    """Calculate Sortino ratio (downside deviation).

    Args:
        returns: Returns Series
        risk_free_rate: Risk-free rate (annualized)
        periods_per_year: Number of periods per year

    Returns:
        Sortino ratio
    """
    excess_returns = returns.mean() * periods_per_year - risk_free_rate
    downside_returns = returns[returns < 0]
    if len(downside_returns) == 0:
        return 0.0
    downside_std = downside_returns.std() * np.sqrt(periods_per_year)
    if downside_std == 0:
        return 0.0
    return excess_returns / downside_std


def calmar_ratio(equity: pd.Series, periods_per_year: int = 252) -> float:
    """Calculate Calmar ratio (return / max drawdown).

    Args:
        equity: Equity curve Series
        periods_per_year: Number of periods per year

    Returns:
        Calmar ratio
    """
    returns = equity.pct_change().dropna()
    ann_return = returns.mean() * periods_per_year
    max_dd = max_drawdown(equity)
    if max_dd == 0:
        return 0.0
    return ann_return / abs(max_dd)


def max_drawdown(equity: pd.Series) -> float:
    """Calculate maximum drawdown.

    Args:
        equity: Equity curve Series

    Returns:
        Maximum drawdown (negative value)
    """
    cummax = equity.expanding().max()
    drawdown = (equity - cummax) / cummax
    return drawdown.min()


def hit_ratio(returns: pd.Series) -> float:
    """Calculate hit ratio (percentage of positive returns).

    Args:
        returns: Returns Series

    Returns:
        Hit ratio (between 0 and 1)
    """
    positive_returns = (returns > 0).sum()
    return positive_returns / len(returns)


def turnover_metric(weights_history: dict) -> float:
    """Calculate average turnover.

    Args:
        weights_history: Dictionary mapping dates to weights Series

    Returns:
        Average turnover per rebalance
    """
    turnovers = []
    prev_weights = None

    for date, weights in sorted(weights_history.items()):
        if prev_weights is not None:
            turnover = (weights - prev_weights).abs().sum()
            turnovers.append(turnover)
        prev_weights = weights.copy()

    return np.mean(turnovers) if turnovers else 0.0


def calculate_metrics(
    returns: pd.Series,
    equity: pd.Series,
    risk_free_rate: float = 0.02,
    periods_per_year: int = 252,
) -> dict:
    """Calculate comprehensive performance metrics.

    Args:
        returns: Returns Series
        equity: Equity curve Series
        risk_free_rate: Risk-free rate
        periods_per_year: Number of periods per year

    Returns:
        Dictionary of performance metrics
    """
    metrics = {
        "total_return": (equity.iloc[-1] / equity.iloc[0]) - 1,
        "annualized_return": (equity.iloc[-1] / equity.iloc[0]) ** (periods_per_year / len(returns))
        - 1,
        "volatility": returns.std() * np.sqrt(periods_per_year),
        "sharpe_ratio": sharpe_ratio(returns, risk_free_rate, periods_per_year),
        "sortino_ratio": sortino_ratio(returns, risk_free_rate, periods_per_year),
        "calmar_ratio": calmar_ratio(equity, periods_per_year),
        "max_drawdown": max_drawdown(equity),
        "hit_ratio": hit_ratio(returns),
    }

    return metrics
