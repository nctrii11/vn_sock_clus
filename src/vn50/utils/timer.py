"""Timing utilities."""

import time
from contextlib import contextmanager
from typing import Generator


@contextmanager
def timer(description: str = "Operation") -> Generator[None, None, None]:
    """Context manager to time an operation.

    Args:
        description: Description of the operation being timed

    Yields:
        None

    Example:
        >>> with timer("Data fetch"):
        ...     # your code here
        Operation 'Data fetch' took 1.23s
    """
    start = time.time()
    yield
    elapsed = time.time() - start
    print(f"Operation '{description}' took {elapsed:.2f}s")
