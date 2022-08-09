"""
Date utilities.

Author: Dominik Zulovec Sajovic, May 2022
"""

from datetime import datetime, date
from argparse import ArgumentTypeError


def valid_date(str_date: str) -> date:
    """Validates if the passed string is a valid date"""
    try:
        return datetime.strptime(str_date, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ArgumentTypeError(
            f"not a valid date: {str_date!r}") from exc


if __name__ == "__main__":
    pass
