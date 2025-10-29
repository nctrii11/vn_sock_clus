"""Markowitz mean-variance optimization."""

import numpy as np
import pandas as pd
import cvxpy as cp


def mean_variance_weights(
    mu: pd.Series,
    Sigma: pd.DataFrame,
    lb: float = 0.0,
    ub: float = 0.15,
    rf: float = 0.0,
    objective: str = "max_sharpe",
    solver: str = "ECOS",
) -> pd.Series:
    """Calculate optimal portfolio weights using Markowitz mean-variance optimization.

    Args:
        mu: Expected returns Series
        Sigma: Covariance matrix DataFrame
        lb: Lower bound on weights (default: 0.0)
        ub: Upper bound on weights (default: 0.15)
        rf: Risk-free rate (default: 0.0)
        objective: Optimization objective ('max_sharpe', 'min_vol', 'max_return')
        solver: CVXPY solver (default: 'ECOS')

    Returns:
        Optimal weights Series (indexed by tickers, sum = 1)
    """
    n = len(mu)

    # Ensure Sigma and mu are aligned
    assert mu.index.equals(Sigma.index) and mu.index.equals(Sigma.columns)

    # Convert to numpy
    mu_vec = mu.values
    Sigma_mat = Sigma.values

    # Define variables
    w = cp.Variable(n)

    # Constraints
    constraints = [
        cp.sum(w) == 1,  # Budget constraint
        w >= lb,  # Long-only (if lb >= 0)
        w <= ub,  # Upper bound
    ]

    # Define objective
    port_var = cp.quad_form(w, Sigma_mat)
    port_mu = mu_vec @ w

    if objective == "min_vol":
        # Minimize variance: minimize w^T Sigma w (equivalent to minimize vol)
        prob = cp.Problem(cp.Minimize(port_var), constraints)
    elif objective == "max_sharpe":
        # Maximize Sharpe ratio: maximize (mu - rf) / sigma
        # Simplify: maximize mu - lambda * variance (linear approximation)
        lambda_risk = 0.5
        prob = cp.Problem(cp.Maximize(port_mu - lambda_risk * port_var), constraints)
    elif objective == "max_return":
        prob = cp.Problem(cp.Maximize(port_mu), constraints)
    else:
        raise ValueError(f"Unknown objective: {objective}")

    # Solve
    try:
        prob.solve(solver="CLARABEL", verbose=False)
    except Exception as e:
        print(f"Warning: CLARABEL failed with {e}. Trying SCS...")
        try:
            prob.solve(solver="SCS", verbose=False, max_iters=50000)
        except Exception as e2:
            print(f"Warning: SCS also failed with {e2}. Trying any solver...")
            prob.solve(verbose=False)

    # Get weights
    weights = pd.Series(w.value, index=mu.index)

    # Replace NaN with 0
    weights = weights.fillna(0.0)

    # Clip to bounds
    weights = weights.clip(lb, ub)

    # Normalize to ensure sum = 1 (handle numerical issues)
    # Iterate to ensure both sum=1 and bounds are respected
    for _ in range(3):  # Iterate up to 3 times
        if weights.sum() > 0:
            weights = weights / weights.sum()
        else:
            # If sum is 0, use equal weights
            weights = pd.Series(1.0 / len(weights), index=mu.index)
            break
        # Clip after normalization
        weights = weights.clip(lb, ub)

    return weights


def min_volatility_weights(
    Sigma: pd.DataFrame,
    lb: float = 0.0,
    ub: float = 0.15,
) -> pd.Series:
    """Calculate minimum volatility portfolio weights.

    Args:
        Sigma: Covariance matrix DataFrame
        lb: Lower bound on weights
        ub: Upper bound on weights

    Returns:
        Optimal weights Series
    """
    # Use equal expected returns as placeholder
    mu = pd.Series(0.0, index=Sigma.index)
    return mean_variance_weights(mu, Sigma, lb=lb, ub=ub, objective="min_vol")


def equal_weight_weights(n_assets: int) -> np.ndarray:
    """Calculate equal weights (1/n for each asset).

    Args:
        n_assets: Number of assets

    Returns:
        Equal weights array
    """
    return np.ones(n_assets) / n_assets
