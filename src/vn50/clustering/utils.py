"""Clustering utility functions."""

import pandas as pd


def cluster_statistics(
    returns: pd.DataFrame,
    labels: pd.Series,
) -> pd.DataFrame:
    """Calculate statistics for each cluster.

    Args:
        returns: Returns DataFrame
        labels: Cluster labels Series

    Returns:
        DataFrame with cluster statistics
    """
    cluster_stats = []

    for cluster_id in labels.unique():
        cluster_assets = labels[labels == cluster_id].index
        cluster_returns = returns[cluster_assets]

        stats = {
            "cluster": cluster_id,
            "n_assets": len(cluster_assets),
            "mean_return": cluster_returns.mean().mean(),
            "volatility": cluster_returns.std().mean(),
            "sharpe": (
                cluster_returns.mean().mean() / cluster_returns.std().mean()
                if cluster_returns.std().mean() > 0
                else 0
            ),
        }
        cluster_stats.append(stats)

    return pd.DataFrame(cluster_stats)
