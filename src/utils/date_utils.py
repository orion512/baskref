"""
Date utilities.

Author: Dominik Zulovec Sajovic, May 2022
"""

from datetime import datetime, date
from argparse import ArgumentTypeError


def valid_date(s: str) -> date:
    """Validates if the passed string is a valid date"""
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        raise ArgumentTypeError("not a valid date: {0!r}".format(s))


if __name__ == "__main__":
    pass
