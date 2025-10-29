"""Tests for Markowitz optimization."""

import numpy as np
import pandas as pd
import pytest

from src.vn50.optimize.markowitz import mean_variance_weights


def test_mean_variance_weights():
    """Test that weights sum to 1 and respect bounds."""
    n = 10
    mu = pd.Series(np.random.randn(n), index=[f"Asset{i}" for i in range(n)])
    Sigma = pd.DataFrame(
        np.random.randn(n, n),
        index=mu.index,
        columns=mu.index,
    )
    Sigma = Sigma @ Sigma.T  # Make PSD

    weights = mean_variance_weights(mu, Sigma, lb=0.0, ub=0.15, objective="max_return")

    # Check sum equals 1
    assert abs(weights.sum() - 1.0) < 1e-5

    # Check bounds (with small tolerance for floating point errors)
    assert (weights >= -1e-10).all()  # Allow tiny negative values from normalization
    assert (weights <= 0.15 + 1e-10).all()  # Allow tiny overflow from normalization


def test_min_volatility_weights():
    """Test minimum volatility optimization."""
    from src.vn50.optimize.markowitz import min_volatility_weights

    n = 5
    Sigma = pd.DataFrame(
        np.random.randn(n, n),
        index=[f"Asset{i}" for i in range(n)],
        columns=[f"Asset{i}" for i in range(n)],
    )
    Sigma = Sigma @ Sigma.T  # Make PSD

    weights = min_volatility_weights(Sigma)

    # Check sum equals 1
    assert abs(weights.sum() - 1.0) < 1e-5
