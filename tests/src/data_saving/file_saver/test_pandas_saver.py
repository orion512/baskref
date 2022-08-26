"""
Holds the tests for the pandas file saver functions

Author: Dominik Zulovec Sajovic - August 2022
"""

import os
import pytest
import pandas as pd
from src.data_saving.file_saver.pandas_saver import (
    check_all_elements_dicts,
    save_file_from_list,
)


root_path = os.path.abspath(
    os.path.join(
        __file__, os.pardir, os.pardir, os.pardir, os.pardir, os.pardir
    )
)


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

    test_saving_to_list = [
        (
            [{"A": 2, "B": "0022"}, {"A": 1, "B": "0011"}],
            os.path.join("tests", "temp", "temp.csv"),
        ),
        (
            [{"A": 2}, {"A": 1}],
            os.path.join("tests", "temp", "temp.csv"),
        ),
        (
            [{"009": "2022-08-09"}, {"009": "2022-28-12"}],
            os.path.join("tests", "temp", "temp.csv"),
        ),
    ]

    @pytest.mark.unittest
    @pytest.mark.parametrize("input_list, file_path", test_saving_to_list)
    def test_save_file_from_list_correct(self, input_list, file_path):
        """Tests the function save_file_from_list."""

        testing_dir = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)

        input_file_path = os.path.join(root_path, testing_dir)
        input_file_full_path = os.path.join(input_file_path, file_name)

        try:
            save_file_from_list(input_list, input_file_full_path)

            read_data = pd.read_csv(input_file_full_path, dtype=str)
            dummy_data = pd.DataFrame(input_list).astype(str)
        finally:
            # Clean the results created by the function
            os.remove(input_file_full_path)
            os.rmdir(input_file_path)

        assert read_data.equals(dummy_data)

    test_saving_to_list_raise = [
        (
            {"A": 2, "B": "0022"},
            os.path.join("tests", "temp", "temp.csv"),
            pytest.raises(ValueError),
        ),
        (
            [{"A": 2}, 3, {"A": 1}],
            os.path.join("tests", "temp", "temp.csv"),
            pytest.raises(ValueError),
        ),
        (
            [{"009": "2022-08-09"}, None, {"009": "2022-28-12"}],
            os.path.join("tests", "temp", "temp.csv"),
            pytest.raises(ValueError),
        ),
    ]

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "input_list, file_path, raise_err",
        test_saving_to_list_raise,
    )
    def test_save_file_from_list_raise(self, input_list, file_path, raise_err):
        """Tests the function save_file_from_list."""

        testing_dir = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)

        input_file_path = os.path.join(root_path, testing_dir)
        input_file_full_path = os.path.join(input_file_path, file_name)

        try:
            with pytest.raises(raise_err.expected_exception):
                save_file_from_list(input_list, input_file_full_path)
        finally:
            # Clean the results created by the function
            if os.path.exists(input_file_path):
                os.remove(input_file_full_path)
                os.rmdir(input_file_path)
