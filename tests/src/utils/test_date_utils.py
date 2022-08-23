"""
Holds the tests for the date utils functions.

Author: Dominik Zulovec Sajovic - August 2022
"""

import os
from datetime import datetime
from argparse import ArgumentTypeError
import pytest
from src.utils.date_utils import valid_date


root_path = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))


class TestDateUtils:
    """Class for date utils tests."""

    test_dates_raise = [
        ("202207-08", pytest.raises(ArgumentTypeError)),
        ("2022-13-08", pytest.raises(ArgumentTypeError)),
        ("2000/07/08", pytest.raises(ArgumentTypeError)),
        ("2022-09-31", pytest.raises(ArgumentTypeError)),
        ("20220708", pytest.raises(ArgumentTypeError)),
    ]

    test_dates_correct = [
        ("2022-07-08", datetime.strptime("2022-07-08", "%Y-%m-%d").date()),
        ("2091-01-03", datetime.strptime("2091-01-03", "%Y-%m-%d").date()),
        ("1978-12-31", datetime.strptime("1978-12-31", "%Y-%m-%d").date()),
    ]

    @pytest.mark.unittest
    @pytest.mark.parametrize("str_date, expected_status", test_dates_raise)
    def test_valid_date_raise(self, str_date, _):
        """Tests the function valid_date."""

        with pytest.raises(ArgumentTypeError):
            _ = valid_date(str_date)

    @pytest.mark.unittest
    @pytest.mark.parametrize("str_date, expected_status", test_dates_correct)
    def test_valid_date_correct(self, str_date, expected_status):
        """Tests the function valid_date."""

        returned_status = valid_date(str_date)
        assert expected_status == returned_status
