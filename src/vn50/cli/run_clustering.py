"""CLI for hierarchical clustering."""

import hydra
from omegaconf import DictConfig
from pathlib import Path
import pandas as pd

from ..utils.logging import setup_logging, task
from ..utils.io import read_parquet, write_parquet
from ..clustering.hclust import hclust_from_distance, get_cluster_labels


@hydra.main(version_base=None, config_path="../../../configs", config_name="experiment_hclust")
def main(cfg: DictConfig) -> None:
    """Main entry point for clustering."""
    logger = setup_logging(cfg.logging.level, cfg.logging.rich)

    # Load distance matrix
    distance_path = Path(cfg.paths.processed) / "distance.parquet"
    with task("Loading distance matrix", logger):
        distance = read_parquet(distance_path)
        logger.info(f"Distance matrix shape: {distance.shape}")

    # Perform hierarchical clustering
    with task("Running hierarchical clustering", logger):
        linkage_matrix, labels = hclust_from_distance(
            distance_matrix=distance,
            method=cfg.linkage,
            n_clusters=cfg.n_clusters,
        )
        logger.info(f"Number of clusters: {len(set(labels))}")

    # Get cluster labels as Series
    cluster_labels = get_cluster_labels(linkage_matrix, len(set(labels)), distance.index)

    # Save cluster labels
    with task("Saving cluster labels", logger):
        write_parquet(
            cluster_labels.to_frame(), Path(cfg.paths.processed) / "cluster_labels.parquet"
        )
        logger.info(f"Cluster labels: {cluster_labels.value_counts().to_dict()}")


if __name__ == "__main__":
    main()
