"""
Util function for the whole package.

Author: Dominik Zulovec Sajovic, May 2022
"""


from datetime import datetime, date
from argparse import ArgumentTypeError


def valid_date(str_date: str) -> date:
    """Validates if the passed string is a valid date"""
    try:
        return datetime.strptime(str_date, "%Y-%m-%d").date()
    except (ValueError, TypeError) as exc:
        raise ArgumentTypeError(f"not a valid date: {str_date!r}") from exc


def str_to_datetime(date_str: str, formats: list[str]) -> datetime:
    """
    tries to convert a string date into a datetime with multiple formats.
    If none of the formats work a default datetime is returned.
    """

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass

    return datetime(1900, 1, 1)
