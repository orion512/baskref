"""
This page contains the basketball reference generator class.

Author: Dominik Zulovec Sajovic, September 2022
"""


from dataclasses import dataclass
from datetime import date
from urllib import parse
from requests_html import HTMLResponse
from src.data_collection.scraper import Scraper


@dataclass
class BasketRefUrlScraper(Scraper):
    """
    Class used for generating the URLs for scraping BasketballRefernce.
    Besides simple generation it also includes scraping and parsing needed
    to provide final urls.
    """

    base_url: str = "https://www.basketball-reference.com"

    # public functions

    def get_game_urls_day(self, game_date: date) -> list:
        """
        Scrapes the urls to every game's boxscore on a specific day.
        :game_date: A game_date to scrape games on
        :return: a list of basketball reference urls
        """

        return self._scrape_game_urls_day(
            self._generate_daily_games_url(game_date)
        )

    # this should be for whole year
    # def get_multiple_game_urls_month(
    #     self, game_list_urls: list
    # ) -> list:
    #     """
    #     Scrapes multiple pages for urls to every game (boxscore).
    #     :game_list_urls: list of URLs containing list of games
    #     :return: returns a list of game urls from Basketball Reference
    #     """

    #     return [
    #         gurl
    #         for url in game_list_urls
    #         for gurl in self.generate_scrape_game_urls_month(url)
    #     ]

    # private functions

    ## scraping functions

    def _scrape_game_urls_day(self, daily_games_url: str) -> list:
        """
        Scrapes the urls to every game's boxscore on a specific day.
        :daily_games_url: Url to the games on that day
        :return: a list of basketball reference urls
        """

        return self.scrape(daily_games_url, self._parse_daily_games)

    ## parsing functions

    def _parse_daily_games(self, daily_games_page: HTMLResponse) -> list:
        """
        Scrapes the urls to every game's boxscore on a specific day.
        :game_date: A game_date to scrape games on
        :return: a list of basketball reference urls
        """

        element_finder = "div.game_summary > p.links"
        game_urls = []

        for p in daily_games_page.html.find(element_finder):
            anch = p.find("a", first=True)
            if anch is not None:
                url = anch.attrs["href"]
                game_urls.append(self.base_url + url)

        return game_urls

    # def generate_scrape_all_months_urls(self, year: int) -> list:
    #     """
    #     Scrapes the urls to every month of a given NBA season
    #     :year: A year representing the year in which the NBA season ends
    #     :return: returns a list of month urls from Basketball Reference
    #     """

    #     # get
    #     main_page = self.get_page(self.generate_season_games_url(year))

    #     # parse
    #     return [
    #         self.base_url + a.attrs["href"]
    #         for a in main_page.html.find("div.filter > div > a")
    #     ]

    # def generate_scrape_game_urls_month(self, month_page: str) -> list:
    #     """
    #     Scrapes the urls to every game (boxscore) from the month webpage.
    #     :page: web page - /leagues/NBA_YEAR_games-MONTH.html
    #     :return: returns a list of game urls from Basketball Reference
    #     """

    #     # get
    #     month_page = self.get_page(month_page)

    #     # parse
    #     element_finder = 'td[data-stat="box_score_text"]'
    #     game_urls = []

    #     for td in month_page.html.find(element_finder):
    #         anch = td.find("a", first=True)
    #         if anch is not None:
    #             url = anch.find("a", first=True).attrs["href"]
    #             game_urls.append(self.base_url + url)

    #     return game_urls

    # def generate_scrape_multiple_game_urls_month(
    #     self, game_list_urls: list
    # ) -> list:
    #     """
    #     Scrapes multiple pages for urls to every game (boxscore).
    #     :game_list_urls: list of URLs containing list of games
    #     :return: returns a list of game urls from Basketball Reference
    #     """

    #     return [
    #         gurl
    #         for url in game_list_urls
    #         for gurl in self.generate_scrape_game_urls_month(url)
    #     ]

    # # helper functions

    def _generate_season_games_url(self, year: int) -> str:
        """Generates the url for all games in a year"""

        if not isinstance(year, int):
            raise ValueError("Year must be a valid integer")

        if year < 1947:
            raise ValueError("Year cannot be less than 1947!")

        return f"{self.base_url}/leagues/NBA_{year}_games.html"

    def _generate_daily_games_url(self, game_date: date) -> str:
        """Generates the url for all games in a given day"""

        if not isinstance(game_date, date):
            raise ValueError("game_date must be a valid date")

        params = parse.urlencode(
            {
                "month": game_date.month,
                "day": game_date.day,
                "year": game_date.year,
            }
        )

        return f"{self.base_url}/boxscores/?{params}"
