"""Hierarchical clustering utilities."""

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, fcluster, linkage
from scipy.spatial.distance import squareform


def hclust_from_distance(
    distance_matrix: pd.DataFrame,
    method: str = "ward",
    n_clusters: int | str = "auto",
) -> tuple[np.ndarray, np.ndarray]:
    """Perform hierarchical clustering from distance matrix.

    Args:
        distance_matrix: Square distance matrix DataFrame
        method: Linkage method ('ward', 'average', 'complete', 'single')
        n_clusters: Number of clusters ('auto' or integer)

    Returns:
        Tuple of (linkage matrix Z, cluster labels)
    """
    # Convert distance matrix to condensed form
    n = len(distance_matrix)
    condensed_distances = squareform(distance_matrix.values, checks=False)

    # Perform linkage
    Z = linkage(condensed_distances, method=method)

    # Determine number of clusters
    if n_clusters == "auto":
        # Simple heuristic: use square root of n_assets or max 10
        n_clusters = min(int(np.sqrt(n)), 10)
        n_clusters = max(n_clusters, 2)  # At least 2 clusters

    # Get cluster labels
    labels = fcluster(Z, n_clusters, criterion="maxclust")

    return Z, labels


def plot_dendrogram(Z: np.ndarray, labels: pd.Index | None = None) -> None:
    """Plot dendrogram from linkage matrix.

    Args:
        Z: Linkage matrix
        labels: Optional labels for leaves
    """
    import matplotlib.pyplot as plt

    plt.figure(figsize=(12, 8))
    dendrogram(Z, labels=labels.tolist() if labels is not None else None)
    plt.xlabel("Asset")
    plt.ylabel("Distance")
    plt.title("Hierarchical Clustering Dendrogram")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()


def get_cluster_labels(
    linkage_matrix: np.ndarray,
    n_clusters: int,
    asset_names: pd.Index,
) -> pd.Series:
    """Get cluster labels as Series.

    Args:
        linkage_matrix: Linkage matrix from hierarchical clustering
        n_clusters: Number of clusters
        asset_names: Asset names (columns from original data)

    Returns:
        Series mapping asset names to cluster labels
    """
    labels = fcluster(linkage_matrix, n_clusters, criterion="maxclust")
    return pd.Series(labels, index=asset_names, name="cluster")
