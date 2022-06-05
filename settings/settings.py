"""

"""


import sys
import logging

from dataclasses import dataclass
from typing import Union
from datetime import date


@dataclass
class Environment:
    name: str


@dataclass
class ProjectLogger:
    level: str
    logger: Union[logging.Logger, None]

    def __post_init__(self):
        """ ... """
        self.logger = logging.getLogger('blogger')
        self.logger.setLevel(self.level)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(self.level)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)


@dataclass
class InLine:
    type: str
    date: date
    namechar: str
    year: int


@dataclass
class Settings:
    """ Class for storing project parameters """

    environment: Environment
    in_line: InLine
    logger: ProjectLogger
