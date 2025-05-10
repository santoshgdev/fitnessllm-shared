"""Logging utilities."""
import json
import logging
from functools import partial
from logging import Logger
from typing import Callable

from beartype.typing import Optional


def setup_logger(name: Optional[str] = None, level: int = logging.DEBUG) -> Logger:
    """Sets up a logger with a console handler.

    Args:
        name (str): Name of the logger.
        level (int): Logging level (e.g., logging.DEBUG, logging.INFO).

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Create a custom logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent adding duplicate handlers if this function is called multiple times
    if logger.hasHandlers():
        return logger

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


logger = setup_logger()


def log_structured(function_name: str, message: str, **kwargs: object) -> None:
    """Helper function to log in structured JSON format.

    Args:
        function_name: Name of the function generating the log
        message: The main log message
        **kwargs: Additional key-value pairs to include in the log
    """
    log_data = {
        "function": function_name,
        "message": f"{function_name}-{message}",
        **kwargs,
    }
    logger.info(json.dumps(log_data))


def create_structured_logger(function_name: str) -> Callable:
    """Create a structured logger for a specific function.

    Args:
        function_name (str): The name of the function to log.

    Returns:
        Callable: A partial function that logs in a structured format.
    """
    return partial(log_structured, function_name=function_name)
