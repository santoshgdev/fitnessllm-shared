"""Logging utilities."""

import logging
import os
from datetime import datetime
from logging import Logger
from typing import Any, Optional
from zoneinfo import ZoneInfo

import google.cloud.logging
from google.auth.exceptions import DefaultCredentialsError
from google.cloud.logging.handlers import CloudLoggingHandler

from fitnessllm_shared.entities.constants import TIMEZONE


class StructuredLogger:
    """Custom logger that adds structured logging capabilities."""

    def __init__(self, name: str | None = None, level: int = logging.DEBUG) -> None:
        """Initialize the structured logger.

        Args:
            name: Name of the logger
            level: Logging level
        """
        self.logger, self.gcp_authenticated = setup_logger(name, level)
        self.name = name or "root"

    def _format_log(
        self,
        level: str,
        message: str,
        data_source: Optional[str] = None,
        user_id: Optional[str] = None,
        **kwargs,
    ) -> dict[str, Any]:
        """Format log entry with structured data."""
        log_data = {
            "level": level,
            "message": message,
            "service": self.name,
            "timestamp": datetime.now(ZoneInfo(TIMEZONE)).isoformat(),
            "gcp_authenticated": self.gcp_authenticated,
        }

        if data_source:
            log_data["data_source"] = data_source
        if user_id:
            log_data["user_id"] = user_id

        # Add any additional fields
        log_data.update(kwargs)

        return log_data

    def info(
        self,
        message: str,
        data_source: Optional[str] = None,
        user_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Log info level message with structured data."""
        log_data = self._format_log("INFO", message, data_source, user_id, **kwargs)
        self.logger.info(log_data)

    def error(
        self,
        message: str,
        data_source: Optional[str] = None,
        user_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Log error level message with structured data."""
        log_data = self._format_log("ERROR", message, data_source, user_id, **kwargs)
        self.logger.error(log_data)

    def warning(
        self,
        message: str,
        data_source: Optional[str] = None,
        user_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Log warning level message with structured data."""
        log_data = self._format_log("WARNING", message, data_source, user_id, **kwargs)
        self.logger.warning(log_data)

    def debug(
        self,
        message: str,
        data_source: Optional[str] = None,
        user_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Log debug level message with structured data."""
        log_data = self._format_log("DEBUG", message, data_source, user_id, **kwargs)
        self.logger.debug(log_data)


def setup_logger(
    name: str | None = None, level: int = logging.DEBUG
) -> tuple[Logger, bool]:
    """Sets up a logger with a console handler and Google Cloud Logging handler.

    Args:
        name (str): Name of the logger.
        level (int): Logging level (e.g., logging.DEBUG, logging.INFO).

    Returns:
        tuple[logging.Logger, bool]: Configured logger instance and authentication status.
    """
    logger = logging.getLogger(name)
    logger.debug("Initializing logger")
    logger.setLevel(level)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("stravalib").setLevel(logging.WARNING)
    logging.getLogger("google.auth._default").setLevel(logging.WARNING)

    # Add console handler if not present
    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    authenticated = False
    try:
        if not any(isinstance(h, CloudLoggingHandler) for h in logger.handlers):
            client = google.cloud.logging.Client()
            cloud_handler = CloudLoggingHandler(client)
            logger.addHandler(cloud_handler)
            authenticated = True
    except DefaultCredentialsError:
        logger.warning(
            "Google Cloud credentials not found. Falling back to console logging only."
        )
    except Exception as e:
        logger.error(f"Unexpected error initializing CloudLoggingHandler: {e}")
    finally:
        # Debug info for troubleshooting
        logger.info(f"GOOGLE_CLOUD_PROJECT: {os.getenv('GOOGLE_CLOUD_PROJECT')}")
        logger.info(
            f"GOOGLE_APPLICATION_CREDENTIALS: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}"
        )
        logger.info(f"GCP Authenticated: {authenticated}")
    return logger, authenticated


# Create default logger instance
logger, gcp_authenticated = setup_logger()

# Create default structured logger instance
structured_logger = StructuredLogger()
