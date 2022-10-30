"""
This page contains the basketball reference class for scraping urls.

- Scrape all teams https://www.basketball-reference.com/teams/
- Scrape all players https://www.basketball-reference.com/players/
- Scrape all games in a year
    - https://www.basketball-reference.com/leagues/NBA_2022_games-april.html
    - scrape all months
    - scrape all games including link to box scores
- Scrape all playoff games in a year
    - https://www.basketball-reference.com/playoffs/NBA_2022_games.html

Author: Dominik Zulovec Sajovic, September 2022
"""


from dataclasses import dataclass
from datetime import date
from urllib import parse
from bs4 import BeautifulSoup
import baskref.data_collection.html_scraper as scr


@dataclass
class BaskRefUrlScraper(scr.HTMLScraper):
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
        :year: A year of the season
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

    def get_game_urls_playoffs(self, year: int) -> list:
        """
        Scrapes the urls to every game's boxscore in a specific postseason.
        :year: A year of the postseason
        :return: a list of basketball reference urls
        """

        return self._scrape_game_urls_playoffs(
            self._generate_playoff_games_url(year)
        )

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

    def _scrape_game_urls_playoffs(self, playoff_games_url: str) -> list:
        """
        Scrapes the urls to every game's boxscore in a specific postseason.
        The parsing function used is the same as the one for months.
        :playoff_games_url: Url to the games in that postseason
        :return: a list of basketball reference urls
        """

        return self.scrape(playoff_games_url, self._parse_monthly_games)

    ## parsing functions

    def _parse_daily_games(self, daily_games_page: BeautifulSoup) -> list:
        """
        Parses the games out of the html containing daily games.
        :game_date: A game_date to scrape games on
        :return: a list of basketball reference urls
        """

        element_finder = "div.game_summary > p.links"
        game_urls = []

        for p in daily_games_page.select(element_finder):
            anch = p.find("a")
            if anch is not None:
                url = anch.attrs["href"]
                game_urls.append(self.base_url + url)  #

        return game_urls

    def _parse_months_in_year(self, yearly_page: BeautifulSoup) -> list:
        """
        Parses the month urls out of the html containing monthly urls.
        :game_date: A game_date to scrape games on
        :return: a list of basketball reference urls
        """

        return [
            self.base_url + a.attrs["href"]
            for a in yearly_page.select("div.filter > div > a")
        ]

    def _parse_monthly_games(self, monthly_games_page: BeautifulSoup) -> list:
        """
        Parses the games out of the html containing monthly games.
        :game_date: A game_date to scrape games on
        :return: a list of basketball reference urls
        """

        element_finder = 'td[data-stat="box_score_text"]'
        game_urls = []

        for td in monthly_games_page.select(element_finder):
            anch = td.find("a")
            if anch is not None:
                url = anch.attrs["href"]
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

    def _generate_playoff_games_url(self, year: int) -> str:

        """Generates the url for all games in a single postseason"""

        if not isinstance(year, int):
            raise ValueError("Year must be a valid integer")

        if year < 1947:
            raise ValueError("Year cannot be less than 1947!")

        return f"{self.base_url}/playoffs/NBA_{year}_games.html"

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
