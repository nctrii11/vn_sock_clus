"""Correlation and distance matrix utilities."""

import numpy as np
import pandas as pd


def rolling_corr(returns: pd.DataFrame, window: int = 60, method: str = "pearson") -> pd.DataFrame:
    """Calculate rolling correlation matrix.

    Args:
        returns: Returns DataFrame
        window: Rolling window size
        method: Correlation method ('pearson' or 'spearman')

    Returns:
        Rolling correlation DataFrame
    """
    return returns.rolling(window).corr(method=method)


def distance_from_corr(corr: pd.DataFrame) -> pd.DataFrame:
    """Calculate distance matrix from correlation matrix using Mantegna distance.

    Formula: d = sqrt(0.5 * (1 - corr))

    Args:
        corr: Correlation matrix DataFrame

    Returns:
        Distance matrix DataFrame with zeros on diagonal
    """
    # Mantegna distance
    distance = np.sqrt(0.5 * (1 - corr))

    # Ensure diagonal is zero and matrix is symmetric
    np.fill_diagonal(distance.values, 0.0)
    distance = (distance + distance.T) / 2

    return distance


def cov_from_corr(corr: pd.DataFrame, vol: pd.Series) -> pd.DataFrame:
    """Calculate covariance matrix from correlation and volatilities.

    Args:
        corr: Correlation matrix
        vol: Volatility Series (annualized)

    Returns:
        Covariance matrix DataFrame
    """
    std_matrix = np.outer(vol, vol)
    cov_matrix = corr * std_matrix
    return pd.DataFrame(cov_matrix, index=corr.index, columns=corr.columns)
