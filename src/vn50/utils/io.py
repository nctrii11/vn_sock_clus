"""I/O utilities for reading and writing data files."""

import pickle
from pathlib import Path
from typing import Any, Optional

import pandas as pd


def read_parquet(path: Path | str) -> pd.DataFrame:
    """Read a Parquet file.

    Args:
        path: Path to parquet file

    Returns:
        DataFrame from parquet file
    """
    return pd.read_parquet(path)


def write_parquet(df: pd.DataFrame, path: Path | str, **kwargs) -> None:
    """Write DataFrame to Parquet file.

    Args:
        df: DataFrame to write
        path: Output path
        **kwargs: Additional arguments to pd.DataFrame.to_parquet()
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(df, pd.Series):
        df.to_frame().to_parquet(path, **kwargs)
    else:
        df.to_parquet(path, **kwargs)


def read_csv(path: Path | str, **kwargs) -> pd.DataFrame:
    """Read a CSV file.

    Args:
        path: Path to CSV file
        **kwargs: Additional arguments to pd.read_csv()

    Returns:
        DataFrame from CSV file
    """
    return pd.read_csv(path, **kwargs)


def write_csv(df: pd.DataFrame, path: Path | str, **kwargs) -> None:
    """Write DataFrame to CSV file.

    Args:
        df: DataFrame to write
        path: Output path
        **kwargs: Additional arguments to pd.DataFrame.to_csv()
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(df, pd.Series):
        df.to_frame().to_csv(path, **kwargs)
    else:
        df.to_csv(path, **kwargs)


def read_pickle(path: Path | str) -> Any:
    """Read a pickle file.

    Args:
        path: Path to pickle file

    Returns:
        Unpickled object
    """
    with open(path, "rb") as f:
        return pickle.load(f)


def write_pickle(obj: Any, path: Path | str) -> None:
    """Write object to pickle file.

    Args:
        obj: Object to pickle
        path: Output path
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(obj, f)
