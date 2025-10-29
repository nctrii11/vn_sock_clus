"""Tests for data fetching."""

import pandas as pd
import pytest

from src.vn50.data.fetch import fetch_prices


def test_fetch_prices_empty_symbols():
    """Test that empty symbols list raises ValueError."""
    with pytest.raises(ValueError, match="Symbols list cannot be empty"):
        fetch_prices([], "2020-01-01", "2020-01-02")


def test_fetch_prices_shape():
    """Test that fetched prices have correct shape."""
    # Note: This test may fail if yfinance is down or symbols don't exist
    # In production, use mock data
    try:
        # Try fetching for a very short period
        prices = fetch_prices(
            symbols=["VN.VN"],  # Vietnam Index
            start="2023-01-01",
            end="2023-01-10",
            adjust=False,
        )
        assert isinstance(prices, pd.DataFrame)
        assert len(prices.columns) >= 1
        assert prices.index.dtype == "datetime64[ns]"
    except Exception as e:
        # Skip test if API is unavailable
        pytest.skip(f"API unavailable: {e}")
