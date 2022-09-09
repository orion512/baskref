"""
Holds the tests for the util.

Author: Dominik Zulovec Sajovic - August 2022
"""

from datetime import datetime
from argparse import ArgumentTypeError
import pytest
from baskref.utils import valid_date


class TestDateUtils:
    """Class for date utils tests."""

    test_dates_raise = [
        ("202207-08", None, pytest.raises(ArgumentTypeError)),
        ("2022-13-08", None, pytest.raises(ArgumentTypeError)),
        ("2000/07/08", None, pytest.raises(ArgumentTypeError)),
        ("2022-09-31", None, pytest.raises(ArgumentTypeError)),
        ("20220708", None, pytest.raises(ArgumentTypeError)),
        (None, None, pytest.raises(ArgumentTypeError)),
        (3, None, pytest.raises(ArgumentTypeError)),
    ]

    test_dates_correct = [
        ("2022-07-08", datetime.strptime("2022-07-08", "%Y-%m-%d").date()),
        ("2091-01-03", datetime.strptime("2091-01-03", "%Y-%m-%d").date()),
        ("1978-12-31", datetime.strptime("1978-12-31", "%Y-%m-%d").date()),
    ]

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "str_date, expected_status, raise_err", test_dates_raise
    )
    def test_valid_date_raise(self, str_date, expected_status, raise_err):
        """Tests the function valid_date."""

        with pytest.raises(raise_err.expected_exception):
            returned_status = valid_date(str_date)
            assert expected_status == returned_status

    @pytest.mark.unittest
    @pytest.mark.parametrize("str_date, expected_status", test_dates_correct)
    def test_valid_date_correct(self, str_date, expected_status):
        """Tests the function valid_date."""

        returned_status = valid_date(str_date)
        assert expected_status == returned_status
