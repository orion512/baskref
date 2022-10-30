"""
This page contains a raw class used for sending GET requests

Author: Dominik Zulovec Sajovic, September 2022
"""


from typing import Callable, Any
from dataclasses import dataclass
import requests
from requests import Response
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


#### I have a jupyter noebook in baskref_db project!!!!!!!!!!!!!!!!!!!!!!!


@dataclass
class HTMLScraper:
    """Class for scraping the web"""

    def scrape(self, url: str, parser_fun: Callable) -> Any:
        """
        This function lays out the skeleton for scraping.
        First sends a GET request to the provided url and then uses
        the provided function to parse out the wanted data.
        """

        page = self.get_page(url)
        soup = BeautifulSoup(page.text, "html.parser")
        return parser_fun(soup)

    @staticmethod
    def parse(html: BeautifulSoup, parser_fun: Callable) -> Any:
        """
        This function lays out the skeleton for parsing.
        Unlike the self.scrape function this function accepts an HTML in the
        form of a BeautifulSoup object and not the url
        (so you are required to get the url contents outside this function).
        Then uses the provided function to parse out the wanted data.
        """

        return parser_fun(html)

    def get_page(self, url: str) -> Response:
        """
        This function scrapes a static webpage from the web.
        It implements a strategy to avoid blocking by the host website.
        1. Normal GET request
        2. GET request with a proxy IP (if available)
        3. GET request with a randomized user-agent
        4. Browser automation (Selenium)

        If the response status code is ok (200-300)
        the function returns a Response object.
        Else it raises an error.
        """

        # 1. Normal GET request
        with requests.Session() as session:
            page = session.get(url)

        if self._is_success_response(page):
            return page

        # TODO: logger here
        # 2. GET request with a proxy IP (if available)
        # TODO: implement proxy here

        if self._is_success_response(page):
            return page

        # 3. GET request with a randomized user-agent and proxy (if available)
        # from fake_useragent import UserAgent

        with requests.Session() as session:
            # TODO: add proxy here as well
            page = session.get(url, headers={"User-Agent": UserAgent().random})

        if self._is_success_response(page):
            return page

        # 4. Browser automation (Selenium, puppeteer)
        # TODO: implement scrape with browser automation
        # TODO: form a requests.Response

        raise ScrapingError(url, page.status_code)

    def _is_success_response(self, resp: Response) -> bool:
        """
        Validates if the passed object is a requests.Response and
        has a valid status code.
        """

        if not isinstance(resp, Response):
            return False

        if not self._is_success_code(resp.status_code):
            return False

        return True

    @staticmethod
    def _is_success_code(code: int) -> bool:
        """
        Validates if the status code is a success.
        It is deemed successful if the code is 2xx.
        """

        if code is None:
            return False

        if not isinstance(code, int):
            raise ValueError("The status code has to be an integer!")

        return 200 <= code < 300


class ScrapingError(Exception):
    """
    Definition for a new type of error when scraping fails.
    This should get raised when we can connect to the domain but the path
    doesn't exist (example 404).
    """

    def __init__(self, url: str, st_code: int):
        """init function"""
        self.message = f"Couldn't scrape {url}. Status code: {st_code}"
        super().__init__(self.message)
