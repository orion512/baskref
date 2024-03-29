"""
Holds the tests for the error utils functions.

Author: Dominik Zulovec Sajovic - August 2022
"""

import pytest
from baskref.exceptions import IllegalArgumentError


class TestErrorUtils:
    """Class for error utils tests."""

    @pytest.mark.unittest
    def test_illegal_arg_type(self):
        """Tests the class IllegalArgumentError is inherited from ValueError"""

        assert issubclass(IllegalArgumentError, ValueError)
