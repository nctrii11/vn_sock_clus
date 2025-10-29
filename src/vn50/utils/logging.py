"""Structured logging utilities."""

import logging
from contextlib import contextmanager
from typing import Optional

FORMAT = "[%(levelname)s] %(asctime)s %(name)s: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(level: str = "INFO", rich: bool = False) -> logging.Logger:
    """Setup logging configuration.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        rich: Whether to use rich console formatting

    Returns:
        Configured logger instance
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=FORMAT,
        datefmt=DATE_FORMAT,
    )
    return logging.getLogger("vn50")


@contextmanager
def task(message: str, logger: Optional[logging.Logger] = None):
    """Context manager for logging task start and completion.

    Args:
        message: Task description
        logger: Optional logger instance (defaults to 'vn50' logger)
    """
    if logger is None:
        logger = logging.getLogger("vn50")
    logger.info(f"{message} ...")
    try:
        yield
        logger.info(f"{message} OK")
    except Exception as e:
        logger.error(f"{message} FAILED - Error: {e}")
        raise
