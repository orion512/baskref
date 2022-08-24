"""
Holds the tests for the pandas file saver functions

Author: Dominik Zulovec Sajovic - August 2022
"""

import os
import pytest
from src.data_saving.file_saver.pandas_saver import (
    check_all_elements_dicts,
    # save_file_from_list,
)


root_path = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))


class TestPandasSaver:
    """Class for pandas saver tester"""

    test_all_elements_raise: list[tuple] = [
        (None, None, pytest.raises(ValueError)),
        ({"a": 2}, None, pytest.raises(ValueError)),
        ({}, None, pytest.raises(ValueError)),
        ("2022-09-31", None, pytest.raises(ValueError)),
        (34, None, pytest.raises(ValueError)),
    ]

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "input_list, expected_status, raise_err", test_all_elements_raise
    )
    def test_check_all_elements_dicts_raise(
        self, input_list, expected_status, raise_err
    ):
        """Tests the function check_all_elements_dicts."""

        with pytest.raises(raise_err.expected_exception):
            returned_status = check_all_elements_dicts(input_list)
            assert expected_status == returned_status

    test_all_elements = [
        ([{}, {}, {}], True),
        ([{"A": 2}, {"A": 1}], True),
        ([{"A": 2}, {"C": 1}], True),
        ([], True),
        ([{"A": 2}, {"A": 1}, 9], False),
        ([None], False),
        ([None, None], False),
        ([1, 2, 3, 4, 5, 6], False),
        ([[1, 2, 3], [14, 5, 6]], False),
        ([[{"A": 2}, {"A": 1}]], False),
    ]

    @pytest.mark.unittest
    @pytest.mark.parametrize("input_list, expected_status", test_all_elements)
    def test_check_all_elements_dicts_correct(
        self, input_list, expected_status
    ):
        """Tests the function check_all_elements_dicts."""

        returned_status = check_all_elements_dicts(input_list)
        assert expected_status == returned_status

    # TODO: test save_file_from_list
