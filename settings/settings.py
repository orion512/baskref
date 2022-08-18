"""
Settings skeleton for the project
"""


import sys
import logging

from dataclasses import dataclass
from typing import Union, Optional
from datetime import date


@dataclass
class Environment:
    """Class for environmental settings"""

    name: str


@dataclass
class InLine:
    """Class for storing arguments passed in-line to run.py"""

    type: str
    date: date
    namechar: str
    year: int
    save: str
    file_path: str


@dataclass
class Saver:
    """Class for data saving settings"""

    file_bucket: str


@dataclass
class Settings:
    """Class for storing project parameters"""

    environment: Environment
    in_line: InLine
    logging_level: str
    logger_name: str

    def __post_init__(self):
        """ """
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(self.logging_level)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(self.logging_level)
        formatter = logging.Formatter(
            "%(asctime)s\t"
            "%(levelname)s\t"
            "%(pathname)s:%(lineno)d\t"
            "%(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
