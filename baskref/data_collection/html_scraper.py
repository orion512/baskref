"""
This page contains a raw class used for sending GET requests

Author: Dominik Zulovec Sajovic, September 2022
"""


from dataclasses import dataclass
import logging
from typing import Callable, Any
import requests
from requests import Response
from requests.exceptions import ProxyError
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


logger = logging.getLogger(__name__)


@dataclass
class HTMLScraper:
    """Class for scraping the web"""

    proxy: str | None = None

    def scrape(self, url: str, parser_fun: Callable) -> Any:
        """
        This function lays out the skeleton for scraping.
        First sends a GET request to the provided url and then uses
        the provided function to parse out the wanted data.
        """

        try:
            page = self.get_page_logic(url)
        except ProxyError as p_err:
            logger.info(f"A Proxy Error occurred {p_err}. Trying again!")
            page = self.get_page_logic(url)

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

    def get_page(
        self, url: str, proxies: dict = None, rand_agent: bool = False
    ) -> Response:
        """
        This function uses as GET request wuth a few optional parameters
        to scrapes a static webpage from the web.
        """

        headers = {"User-Agent": UserAgent().random} if rand_agent else None

        with requests.Session() as session:
            page = session.get(url, proxies=proxies, headers=headers)

        return page

    def get_page_browser(self, url: str, proxies: dict = None) -> Response:
        """
        This function uses a browser aurtomation tool to navigate to the
        specified url and pull the html code.
        """

    def get_page_logic(self, url: str) -> Response:
        """
        This function scrapes a static webpage from the web.
        It implements a strategy to avoid blocking by the host website.
        All requests use a proxy if specified.
        1. Normal GET request
        2. GET request with a randomized user-agent
        3. Browser automation (Selenium, pypeteer)

        If the response status code is ok (200-300)
        the function returns a Response object.
        Else it raises an error.
        """

        # 1. Normal GET request
        page = self.get_page(url, proxies=self._proxies())

        if self._is_success_response(page):
            return page

        logger.debug(
            f"[1] Normal scrape failed ({page.status_code}). "
            f"Proxy used: {self.proxy}"
        )

        # 2. GET request with a randomized user-agent
        page = self.get_page(url, proxies=self._proxies(), rand_agent=True)

        if self._is_success_response(page):
            return page

        logger.debug(
            f"[2] Random user agent scrape failed ({page.status_code}). "
            f"Proxy used: {self.proxy}"
        )

        # 3. Browser automation (Selenium, puppeteer)
        # TODO: self.get_page_browser(url)
        # TODO: form a requests.Response

        if page.status_code == 429:
            raise TooManyRequests(url, page.status_code)
        if page.status_code == 403:
            raise PermissionDenied(url, page.status_code)

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

    def _proxies(self) -> dict | None:
        """If a proxy is passed"""
        if self.proxy:
            return {
                "https": self.proxy,
                "http": self.proxy,
            }
        return None


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


class TooManyRequests(ScrapingError):
    """
    Definition for a new type of error when scraping fails due to
    the server not accepting the amount of requests.
    """


class PermissionDenied(ScrapingError):
    """
    Definition for a new type of error when scraping fails due to
    the server not accepting the amount of requests.
    """
