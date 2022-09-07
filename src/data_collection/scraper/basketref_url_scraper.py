"""
This page contains the basketball reference generator class.

Author: Dominik Zulovec Sajovic, September 2022
"""


from dataclasses import dataclass
from datetime import date
from urllib import parse
from requests_html import HTMLResponse
import src.data_collection.scraper.html_scraper as scr


@dataclass
class BasketRefUrlScraper(scr.HTMLScraper):
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

    def get_game_urls_year(self, year: int) -> list:
        """
        Scrapes the urls to every game's boxscore on a specific day.
        :game_date: A game_date to scrape games on
        :return: a list of basketball reference urls
        """

        # scrape yearly url for monthly urls
        monthly_urls = self._scrape_month_urls(
            self._generate_season_games_url(year)
        )

        # scrape monthly urls for game data
        return [
            gurl
            for murl in monthly_urls
            for gurl in self._scrape_game_urls_month(murl)
        ]

    # private functions

    ## scraping functions

    def _scrape_game_urls_day(self, daily_games_url: str) -> list:
        """
        Scrapes the urls to every game's boxscore on a specific day.
        :daily_games_url: Url to the games on that day
        :return: a list of basketball reference urls
        """

        return self.scrape(daily_games_url, self._parse_daily_games)

    def _scrape_month_urls(self, yearly_games_url: str) -> list:
        """
        Scrapes the urls to every month with games in a single year (season)
        :yearly_games_url: Url to list of months in a season
        :return: a list of basketball reference urls
        """

        return self.scrape(yearly_games_url, self._parse_months_in_year)

    def _scrape_game_urls_month(self, month_games_url: str) -> list:
        """
        Scrapes the urls to every game's boxscore in a specific month
        in a year.
        :month_games_url: Url to the games in that month
        :return: a list of basketball reference urls
        """

        return self.scrape(month_games_url, self._parse_monthly_games)

    ## parsing functions

    def _parse_daily_games(self, daily_games_page: HTMLResponse) -> list:
        """
        Parses the games out of the html containing daily games.
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

    def _parse_months_in_year(self, yearly_page: HTMLResponse) -> list:
        """
        Parses the month urls out of the html containing monthly urls.
        :game_date: A game_date to scrape games on
        :return: a list of basketball reference urls
        """

        return [
            self.base_url + a.attrs["href"]
            for a in yearly_page.html.find("div.filter > div > a")
        ]

    def _parse_monthly_games(self, monthly_games_page: HTMLResponse) -> list:
        """
        Parses the games out of the html containing monthly games.
        :game_date: A game_date to scrape games on
        :return: a list of basketball reference urls
        """

        element_finder = 'td[data-stat="box_score_text"]'
        game_urls = []

        for td in monthly_games_page.html.find(element_finder):
            anch = td.find("a", first=True)
            if anch is not None:
                url = anch.find("a", first=True).attrs["href"]
                game_urls.append(self.base_url + url)

        return game_urls

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
