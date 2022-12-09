"""
Holds the tests for the scraper class

Author: Dominik Zulovec Sajovic - September 2022
"""


from unittest.mock import patch
import pytest
from requests import Response
from baskref.data_collection.html_scraper import (
    HTMLScraper,
    ScrapingError,
)

# pylint: disable=protected-access


class TestScraper:
    """Class for Scraper class"""

    @staticmethod
    def _generate_response(html_cont: str, status_code: int) -> Response:
        """Generates a requests.Response to be used for testing"""

        res = Response()
        res._content = html_cont.encode("utf-8")
        res.status_code = status_code

        return res

    test_get_pages: list[tuple] = [
        ("https://google.com", "<p>Some HTML!</p>", 200),
        ("https://www.basketball-reference.com", "<div>27.2 ppg</div>", 200),
        ("https://nba.com", "<span>Some HTML!</span>", 201),
    ]

    @pytest.mark.unittest
    @patch("requests.Session.get")
    @pytest.mark.parametrize("input_url, website_html, code", test_get_pages)
    def test_get_page(self, req_mock, input_url, website_html, code):
        """Tests the function get_page."""

        req_mock.return_value = self._generate_response(website_html, code)

        scp = HTMLScraper()

        page = scp.get_page(input_url)

        assert page.text == website_html
        assert page.status_code == code

    test_get_pages_raise: list[tuple] = [
        (404, None, pytest.raises(ScrapingError)),
        (100, None, pytest.raises(ScrapingError)),
        (500, None, pytest.raises(ScrapingError)),
        (400, None, pytest.raises(ScrapingError)),
    ]

    @pytest.mark.unittest
    @patch("requests.Session.get")
    @pytest.mark.parametrize(
        "code, expected_status, raise_err", test_get_pages_raise
    )
    def test_get_page_raise(self, req_mock, code, expected_status, raise_err):
        """Tests the function get_page."""

        req_mock.return_value = self._generate_response("<div>ok</div>", code)

        scp = HTMLScraper()

        with pytest.raises(raise_err.expected_exception):
            returned_status = scp.get_page_logic("https://fake.url")
            assert expected_status == returned_status

    test_succ_codes: list[tuple] = [
        (0, False),
        (20, False),
        (190, False),
        (200, True),
        (201, True),
        (202, True),
        (220, True),
        (299, True),
        (300, False),
        (404, False),
        (500, False),
    ]

    @pytest.mark.unittest
    @pytest.mark.parametrize("input_code, expected_status", test_succ_codes)
    def test_is_success_code(self, input_code, expected_status):
        """Tests the function scrape_game_urls_day."""

        scp = HTMLScraper()

        returned_status = scp._is_success_code(input_code)
        assert expected_status == returned_status


class TestScrapingError:
    """Class for ScrapingError class"""

    test_scraping_errors: list[tuple] = [
        ("some_url", 404),
        ("http://neki.com", 404),
        ("https://neki.com", 301),
        ("www.neki.com", 500),
        ("https://neki.com/some_path/some_other_oath", None),
    ]

    @pytest.mark.unittest
    @pytest.mark.parametrize("input_url, input_code", test_scraping_errors)
    def test_scraping_error(self, input_url, input_code):
        """Tests the message in the ScrapingError"""

        exp = ScrapingError(input_url, input_code)

        assert input_url in exp.message
        assert str(input_code) in exp.message
