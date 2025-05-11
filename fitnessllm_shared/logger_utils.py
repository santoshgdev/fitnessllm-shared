"""Logging utilities for structured logging in Python."""

import logging
import os

from google.auth.exceptions import DefaultCredentialsError
from google.cloud import logging as cloud_logging
from google.cloud.logging.handlers import CloudLoggingHandler


def is_running_in_gcp():
    """Check if the code is running in Google Cloud Platform (GCP)."""
    return os.getenv("K_SERVICE") or os.getenv("GOOGLE_CLOUD_PROJECT")


class StructuredLogger:
    """Custom logger that adds structured logging capabilities."""

    def __init__(self):
        """Initialize the structured logger."""
        self.logger = logging.getLogger("fitnessllm")
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False  # Prevent double logging

        # Remove all existing handlers to avoid duplicates
        for handler in list(self.logger.handlers):
            self.logger.removeHandler(handler)

        self.gcp_authenticated = False

        if is_running_in_gcp():
            try:
                client = cloud_logging.Client()
                cloud_handler = CloudLoggingHandler(client)
                self.logger.addHandler(cloud_handler)
                self.gcp_authenticated = True
            except DefaultCredentialsError:
                self.logger.warning(
                    "Google Cloud credentials not found. Falling back to console logging only."
                )
                self.logger.addHandler(logging.StreamHandler())
        else:
            self.logger.addHandler(logging.StreamHandler())

    def info(self, message, **kwargs):
        """Logs an informational message.

        Args:
            message (str): The message to log.
            **kwargs: Additional context to include in the log entry.
        """
        self.logger.info(message, extra=kwargs)

    def warning(self, message, **kwargs):
        """Logs a warning message.

        Args:
            message (str): The message to log.
            **kwargs: Additional context to include in the log entry.
        """
        self.logger.warning(message, extra=kwargs)

    def error(self, message, **kwargs):
        """Logs an error message.

        Args:
            message (str): The message to log.
            **kwargs: Additional context to include in the log entry.
        """
        self.logger.error(message, extra=kwargs)

    def debug(self, message, **kwargs):
        """Logs a debug message.

        Args:
            message (str): The message to log.
            **kwargs: Additional context to include in the log entry.
        """
        self.logger.debug(message, extra=kwargs)

    def critical(self, message, **kwargs):
        """Logs a critical message.

        Args:
            message (str): The message to log.
            **kwargs: Additional context to include in the log entry.
        """
        self.logger.critical(message, extra=kwargs)


# Export a singleton instance
structured_logger = StructuredLogger()
