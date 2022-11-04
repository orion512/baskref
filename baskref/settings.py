"""
Settings skeleton for the project
"""


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
    proxy: str


@dataclass
class Settings:
    """Class for storing project parameters"""

    in_line: InLine
