"""Tests for returns module."""

import numpy as np
import pandas as pd
import pytest

from src.vn50.features.returns import make_returns


def test_make_returns_shapes():
    """Test that returns have correct shape."""
    prices = pd.DataFrame(
        {"AAA": [100, 101, 102, 103], "BBB": [50, 51, 49, 52]},
        index=pd.date_range("2020-01-01", periods=4),
    )
    returns = make_returns(prices)
    assert returns.shape[0] == prices.shape[0] - 1
    assert returns.shape[1] == prices.shape[1]


def test_make_returns_log():
    """Test log returns calculation."""
    prices = pd.DataFrame({"A": [100, 105, 110, 108]}, index=pd.date_range("2020-01-01", periods=4))
    returns = make_returns(prices, kind="log")
    assert isinstance(returns, pd.DataFrame)
    assert len(returns) == 3


def test_make_returns_arith():
    """Test arithmetic returns calculation."""
    prices = pd.DataFrame({"A": [100, 105, 110, 108]}, index=pd.date_range("2020-01-01", periods=4))
    returns = make_returns(prices, kind="arith")
    assert isinstance(returns, pd.DataFrame)
    assert len(returns) == 3
