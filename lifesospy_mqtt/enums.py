"""
This module contains all enumerations used by this application.
"""

import logging
from lifesospy.enums import IntEnumEx


class LoggerLevel(IntEnumEx):
    """Severity level for logger."""
    Critical = logging.CRITICAL
    Error = logging.ERROR
    Warning = logging.WARNING
    Info = logging.INFO
    Debug = logging.DEBUG
    NotSet = logging.NOTSET


class OnOff(IntEnumEx):
    """On / Off state."""
    Off = int(False)
    On = int(True)

class OpenClosed(IntEnumEx):
    """Open / Closed state."""
    Open = int(False)
    Closed = int(True)
