"""
Provides configurable filtering settings for the logging system.
"""

import logging
from lifesospy_mqtt.config import Config


class Filter(logging.Filter):
    """Performs our custom filtering."""

    def __init__(self, config: Config):
        super().__init__()
        self._config = config

    def filter(self, record: logging.LogRecord) -> bool:
        """Determine if record meets minimum severity level."""
        for namespace in self._config.logger.namespaces.items():
            if record.name.startswith(namespace[0]):
                return record.levelno >= namespace[1].value
        return record.levelno >= self._config.logger.default.value


def configure(config: Config):
    """Configure logging to filter using the specified settings."""

    logger = logging.getLogger('')
    logger.setLevel(logging.NOTSET)

    for handler in logging.root.handlers:
        handler.setLevel(logging.NOTSET)
        handler.addFilter(Filter(config))
