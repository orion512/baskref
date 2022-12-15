"""
Util function for the whole package.

Author: Dominik Zulovec Sajovic, May 2022
"""


from datetime import datetime, date
from argparse import ArgumentTypeError
from typing import Any


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


def num(char: str | None) -> float | int | None:
    """
    tries to convert a string into an int and returns it.
    If the conversion fails it tries to convert the string into a float
    and returns it.
    If the string is None it return None.
    """
    if char is None:
        return None

    try:
        return int(char)
    except ValueError:
        return float(char)


def broadcast(list_dicts: list[dict], key: str, val: Any) -> list[dict]:
    """broadcasts a value into every dictionary in a list"""

    for dic in list_dicts:
        dic[key] = val

    return list_dicts
