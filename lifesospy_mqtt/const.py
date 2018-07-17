"""
This module contains all common constants used by this application.
"""

import os

# Project metadata
PROJECT_NAME = 'lifesospy_mqtt'
PROJECT_DESCRIPTION = "MQTT client to report state of LifeSOS security system and devices."
PROJECT_VERSION = '0.1.0'
__version__ = PROJECT_VERSION

# Exit codes. Only have proper definitions in Unix; just pick an arbitrary value otherwise
EX_OK = getattr(os, 'EX_OK', 0)
EX_NOHOST = getattr(os, 'EX_NOHOST', 68)
EX_CONFIG = getattr(os, 'EX_CONFIG', 78)
