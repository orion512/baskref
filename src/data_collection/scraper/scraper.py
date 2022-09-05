"""
This page contains a raw class used for sending GET requests

Author: Dominik Zulovec Sajovic, September 2022
"""


from typing import Callable, Any, Union
from dataclasses import dataclass
from requests.exceptions import RequestException
from requests_html import HTMLSession, HTMLResponse, Element


@dataclass
class Scraper:
    """Class for scraping the web"""

    def scrape(self, url: str, parser_fun: Callable) -> Any:
        """
        This function lays out the skeleton for scraping.
        First sends a GET request to the provided url and then uses
        the provided function to parse out the wanted data.
        """

        page = self.get_page(url)
        return parser_fun(page)

    @staticmethod
    def parse(html: HTMLResponse, parser_fun: Callable) -> Any:
        """
        This function lays out the skeleton for parsing.
        Unlike the self.scrape function this function accepts the
        HTMLResponse and not the url (so you are required to get the url
        contents outside this function). Then uses
        the provided function to parse out the wanted data.
        """

        return parser_fun(html)

    def simple_parse(
        self, html: Element, finder: str, txt: bool = True
    ) -> Union[str, Element]:
        """
        Provided an HTML Element object and a CSS finder
        it parses out the text (or whole element) of the first element found.
        Sometime the page doesn't include attendance in which case the
        method return None.
        :return: the text of the element
        """

        ele = html.find(finder, first=True)

        if txt:
            return ele.text

        return ele

    def get_page(self, url: str) -> HTMLResponse:
        """
        Makes a get request to the provided URL and
        return a response if status code is ok (200).
        """

        with HTMLSession() as session:
            try:
                page = session.get(url)
            except RequestException as err:
                raise ScrapingConnError(url) from err

            if self._is_success_code(page.status_code):
                return page

            raise ScrapingError(url, page.status_code)

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


class ScrapingConnError(Exception):
    """Definition for a new type of error when connection fails"""

    def __init__(self, url: str):
        """init function"""
        self.message = f"Connection to {url} failed"
        super().__init__(self.message)
