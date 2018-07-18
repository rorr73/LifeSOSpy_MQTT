"""
Provides configurable filtering settings for the logging system.
"""

import logging
from lifesospy_mqtt.config import Config


class Filter(logging.Filter):
    """Performs our custom filtering."""

    def __init__(self, config: Config, verbose: bool):
        super().__init__()
        self._config = config
        self._verbose = verbose

    def filter(self, record: logging.LogRecord) -> bool:
        """Determine if record meets minimum severity level."""
        if self._verbose:
            return record.levelno >= logging.DEBUG
        for namespace in self._config.logger.namespaces.items():
            if record.name.startswith(namespace[0]):
                return record.levelno >= namespace[1].value
        return record.levelno >= self._config.logger.default.value
