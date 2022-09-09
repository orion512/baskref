"""
Settings skeleton for the project
"""


import os
import sys
import logging

from dataclasses import dataclass
from datetime import date


@dataclass
class InLine:
    """Class for storing command line passed arguments"""

    type: str
    date: date
    namechar: str
    year: int
    file_path: str


@dataclass
class Settings:
    """Class for storing project parameters"""

    in_line: InLine

    def __post_init__(self):
        """Runs imiidiately after the initialization"""

        log_level = os.getenv("LOG_LEVEL", "INFO")
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        formatter = logging.Formatter(
            "%(asctime)s\t"
            "%(levelname)s\t"
            "%(pathname)s:%(lineno)d\t"
            "%(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
