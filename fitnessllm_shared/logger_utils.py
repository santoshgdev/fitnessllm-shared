"""Logging utilities for structured logging in Python."""

import logging
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from google.auth.exceptions import DefaultCredentialsError
from google.cloud import logging as cloud_logging
from google.cloud.logging.handlers import CloudLoggingHandler

from fitnessllm_shared.entities.constants import TIMEZONE


def is_running_in_gcp():
    """Check if the code is running in Google Cloud Platform (GCP).

    Returns:
        bool: True if running in GCP, False otherwise.
    """
    return bool(os.getenv("CLOUD_RUN_JOB"))


class StructuredLogger:
    """Custom logger that adds structured logging capabilities."""

    def __init__(self):
        """Initialize the structured logger.

        Sets up the logger, attaches appropriate handlers for GCP or local environments,
        and determines the current git commit hash and authentication status.
        """
        self.logger = logging.getLogger("fitnessllm")
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False  # Prevent double logging
        self.shared_commit_hash = os.getenv("FITNESSLLM_SHARED_COMMIT_HASH")

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

    def _format_log(self, level, message, **kwargs):
        """Format the log entry as a structured dictionary.

        Args:
            level (str): The log level (e.g., 'INFO', 'ERROR').
            message (str): The log message.
            **kwargs: Additional context to include in the log entry.

        Returns:
            dict: Structured log entry including commit hash and authentication status.
        """
        log_data = {
            "level": level,
            "message": message,
            "timestamp": datetime.now(ZoneInfo(TIMEZONE)).isoformat(),
            "commit_hash": self.shared_commit_hash,
            "gcp_authenticated": self.gcp_authenticated,
        }
        log_data.update(kwargs)
        return log_data

    def info(self, message, **kwargs):
        """Log an informational message with structured data.

        Args:
            message (str): The message to log.
            **kwargs: Additional context to include in the log entry.
        """
        self.logger.info(self._format_log("INFO", message, **kwargs))

    def warning(self, message, **kwargs):
        """Log a warning message with structured data.

        Args:
            message (str): The message to log.
            **kwargs: Additional context to include in the log entry.
        """
        self.logger.warning(self._format_log("WARNING", message, **kwargs))

    def error(self, message, **kwargs):
        """Log an error message with structured data.

        Args:
            message (str): The message to log.
            **kwargs: Additional context to include in the log entry.
        """
        self.logger.error(self._format_log("ERROR", message, **kwargs))

    def debug(self, message, **kwargs):
        """Log a debug message with structured data.

        Args:
            message (str): The message to log.
            **kwargs: Additional context to include in the log entry.
        """
        self.logger.debug(self._format_log("DEBUG", message, **kwargs))

    def critical(self, message, **kwargs):
        """Log a critical message with structured data.

        Args:
            message (str): The message to log.
            **kwargs: Additional context to include in the log entry.
        """
        self.logger.critical(self._format_log("CRITICAL", message, **kwargs))


structured_logger = StructuredLogger()
