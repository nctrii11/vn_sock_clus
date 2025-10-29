"""Portfolio optimization constraints."""

import numpy as np
import pandas as pd


def apply_weight_bounds(weights: pd.Series, lb: float = 0.0, ub: float = 1.0) -> pd.Series:
    """Apply weight bounds to portfolio weights.

    Args:
        weights: Portfolio weights Series
        lb: Lower bound
        ub: Upper bound

    Returns:
        Bounded weights Series
    """
    return weights.clip(lb, ub)


def calculate_turnover(old_weights: pd.Series, new_weights: pd.Series) -> float:
    """Calculate portfolio turnover.

    Args:
        old_weights: Previous weights
        new_weights: New weights

    Returns:
        Turnover (sum of absolute weight changes)
    """
    return abs(new_weights - old_weights).sum()


def apply_turnover_limit(
    target_weights: pd.Series,
    current_weights: pd.Series,
    max_turnover: float,
) -> pd.Series:
    """Apply turnover limit to portfolio rebalancing.

    Args:
        target_weights: Target weights
        current_weights: Current weights
        max_turnover: Maximum allowed turnover

    Returns:
        Weights adjusted for turnover constraint
    """
    turnover = calculate_turnover(current_weights, target_weights)

    if turnover <= max_turnover:
        return target_weights

    # Reduce weights proportionally
    diff = target_weights - current_weights
    scale = max_turnover / turnover
    adjusted_weights = current_weights + scale * diff

    # Ensure budget constraint
    adjusted_weights = adjusted_weights / adjusted_weights.sum()

    return adjusted_weights
