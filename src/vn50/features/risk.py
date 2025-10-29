"""Risk metrics calculation utilities."""

import numpy as np
import pandas as pd
from scipy.linalg import LinAlgError
from scipy.stats import lognorm


def volatility(returns: pd.DataFrame, window: int = 20, annualized: bool = True) -> pd.DataFrame:
    """Calculate rolling volatility.

    Args:
        returns: Returns DataFrame
        window: Rolling window size
        annualized: Whether to annualize volatility (default: True)

    Returns:
        Rolling volatility DataFrame
    """
    vol = returns.rolling(window).std()
    if annualized:
        vol = vol * np.sqrt(252)
    return vol


def max_drawdown(prices: pd.DataFrame) -> pd.Series:
    """Calculate maximum drawdown for each asset.

    Args:
        prices: Prices DataFrame

    Returns:
        Maximum drawdown Series
    """
    cummax = prices.cummax()
    drawdown = (prices - cummax) / cummax
    return drawdown.min()


def var(returns: pd.DataFrame, confidence: float = 0.05) -> pd.Series:
    """Calculate Value at Risk (VaR).

    Args:
        returns: Returns DataFrame
        confidence: Confidence level (default: 0.05 for 95% VaR)

    Returns:
        VaR Series
    """
    return returns.quantile(confidence, axis=0)


def cvar(returns: pd.DataFrame, confidence: float = 0.05) -> pd.Series:
    """Calculate Conditional Value at Risk (CVaR).

    Args:
        returns: Returns DataFrame
        confidence: Confidence level (default: 0.05 for 95% CVaR)

    Returns:
        CVaR Series
    """
    var_values = returns.quantile(confidence, axis=0)
    return returns[returns <= var_values].mean()


def ann_cov(returns: pd.DataFrame, ann_factor: int = 252) -> pd.DataFrame:
    """Calculate annualized covariance matrix.

    Args:
        returns: Returns DataFrame
        ann_factor: Annualization factor (default: 252 for daily data)

    Returns:
        Annualized covariance matrix DataFrame
    """
    return returns.cov() * ann_factor


def shrink_cov(cov: pd.DataFrame, method: str = "lw") -> pd.DataFrame:
    """Apply covariance shrinkage.

    Args:
        cov: Covariance matrix DataFrame
        method: Shrinkage method ('lw', 'oas', 'none')

    Returns:
        Shrunk covariance matrix DataFrame
    """
    if method == "none":
        return cov

    cov_matrix = cov.values
    n_assets = len(cov_matrix)

    try:
        if method == "lw" or method == "lw2":
            # Ledoit-Wolf shrinkage
            from sklearn.covariance import LedoitWolf

            lw = LedoitWolf()
            cov_shrunk = lw.fit(cov_matrix)
            return pd.DataFrame(
                cov_shrunk.covariance_,
                index=cov.index,
                columns=cov.columns,
            )
        elif method == "oas":
            # Oracle Approximating Shrinkage
            from sklearn.covariance import OAS

            oas = OAS()
            cov_shrunk = oas.fit(cov_matrix)
            return pd.DataFrame(
                cov_shrunk.covariance_,
                index=cov.index,
                columns=cov.columns,
            )
        else:
            raise ValueError(f"Unknown shrinkage method: {method}")
    except (ImportError, LinAlgError) as e:
        print(f"Warning: Shrinkage failed with {e}. Returning original covariance.")
        return cov
