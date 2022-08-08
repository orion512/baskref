"""
This page contains the class which is used to scrape data
from basketball reference website.

- Scrape all teams https://www.basketball-reference.com/teams/
- Scrape all players https://www.basketball-reference.com/players/
- Scrape all games in a year
    - https://www.basketball-reference.com/leagues/NBA_2022_games-april.html
    - scrape all months
    - scrape all games including link to box scores
- Scrape all playoff games in a year
    - https://www.basketball-reference.com/playoffs/NBA_2022_games.html

Author: Dominik Zulovec Sajovic, May 2022
"""

import urllib.parse

from dataclasses import dataclass
from requests import Response
from requests_html import HTMLSession, Element
from datetime import datetime, date
from typing import Tuple, Optional, Dict, Union
from urllib import parse


@dataclass
class BasketballReference:
    """Class for scraping & Parsing basketball-reference.com"""

    base_url: str = "https://www.basketball-reference.com"

    @classmethod
    def generate_season_games_url(cls, year: int) -> str:
        """Generates the url for all games in a year"""
        return f"{cls.base_url}/leagues/NBA_{year}_games.html"

    @classmethod
    def generate_daily_games_url(cls, date: date) -> str:
        """Generates the url for all games in a given day"""

        params = urllib.parse.urlencode(
            {"month": date.month, "day": date.day, "year": date.year}
        )

        return f"{cls.base_url}/boxscores/?{params}"

    def scrape_game_urls_day(self, date: date) -> list:
        """
        Scrapes the urls to every game's boxscore on a specific day.
        :date: A date to scrape games on
        :return: a list of basketball reference urls
        """
        element_finder = "div.game_summary > p.links"

        game_urls = []

        day_page = self._get_page(self.generate_daily_games_url(date))
        for p in day_page.html.find(element_finder):
            anch = p.find("a", first=True)
            if anch is not None:
                url = anch.attrs["href"]
                game_urls.append(self.base_url + url)

        return game_urls

    def scrape_all_months_urls(self, year: int) -> list:
        """
        Scrapes the urls to every month of a given NBA season
        :year: A year representing the year in which the NBA season ends
        :return: returns a list of month urls from Basketball Reference
        """

        main_page = self._get_page(self.generate_season_games_url(year))
        return [
            self.base_url + a.attrs["href"]
            for a in main_page.html.find("div.filter > div > a")
        ]

    def scrape_game_urls_month(self, page: str) -> list:
        """
        Scrapes the urls to every game (boxscore) from the month webpage.
        :page: web page - /leagues/NBA_YEAR_games-MONTH.html
        :return: returns a list of game urls from Basketball Reference
        """

        element_finder = 'td[data-stat="box_score_text"]'
        game_urls = []

        month_page = self._get_page(page)
        for td in month_page.html.find(element_finder):
            anch = td.find("a", first=True)
            if anch is not None:
                url = anch.find("a", first=True).attrs["href"]
                game_urls.append(self.base_url + url)

        return game_urls

    def scrape_multiple_game_urls_month(self, game_list_urls: list) -> list:
        """
        Scrapes multiple pages for urls to every game (boxscore).
        :game_list_urls: list of URLs containing list of games
        :return: returns a list of game urls from Basketball Reference
        """

        return [
            gurl
            for url in game_list_urls
            for gurl in self.scrape_game_urls_month(url)
        ]

    def scrape_game_data(self, game_url: str) -> dict:
        """
        Scrapes the data for the given game web page.
        :game_url: a Basketball Reference URL to a game page
        :return: returns a dictionary of game data
        """

        game_page = self._get_page(game_url)

        # Team names
        home_team_fn, home_team_sn = self._parse_team_name(game_page, "home")
        away_team_fn, away_team_sn = self._parse_team_name(game_page, "away")

        # game meta data
        game_time, arena_name = self._parse_game_meta_data(game_page)
        attendance = self._parse_attendance(game_page)

        game_id = self._parse_game_id(game_url)

        game_dic = {
            "game_id": game_id,
            "home_team": home_team_sn,
            "away_team": away_team_sn,
            "home_team_full_name": home_team_fn,
            "away_team_full_name": away_team_fn,
            "game_time": game_time,
            "arena_name": arena_name,
            "attendance": attendance,
            "game_url": game_url,
        }

        home_basic_dic = self._parse_basic_stats(
            game_page, "home", home_team_sn
        )

        away_basic_dic = self._parse_basic_stats(
            game_page, "away", away_team_sn
        )

        game_dic = {**game_dic, **home_basic_dic, **away_basic_dic}

        home_advanced_dic = self._parse_advanced_stats(
            game_page, "home", home_team_sn
        )

        away_advanced_dic = self._parse_advanced_stats(
            game_page, "away", away_team_sn
        )

        game_dic = {**game_dic, **home_advanced_dic, **away_advanced_dic}

        return game_dic

    def scrape_multiple_games_data(self, game_urls: list) -> list:
        """
        Scrapes the data for all the game urls provided
        :game_urls: list of box score game urls from basketball reference
        :return: returns a list of dictionaries with game data
        """

        return [self.scrape_game_data(url) for url in game_urls]

    # Private Methods

    @staticmethod
    def _get_page(url: str) -> Response:
        """
        Makes a get request to the provided URL and
        return a response if status code is ok (200).
        """

        with HTMLSession() as session:
            page = session.get(url)
            if page.status_code == 200:
                return page
            else:
                raise Exception(
                    f"Couldn't scrape {url}. Status code: {page.status_code}"
                )

    def _simple_parse(
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
        else:
            return ele

    def _parse_team_name(self, html: Response, team: str) -> Tuple[str, str]:
        """
        Provided the BR game page and the team parameter it parses out
        the team short and long names.
        :team: indicates the home or away team
        :return: Tuple(team long name, team short name)
        """

        if team not in ["home", "away"]:
            raise ValueError('The team argument can only be "home" or "away"')

        team_idx = 1 if team == "home" else 2

        team_anchor = html.html.find(
            f"#content > div.scorebox > div:nth-child({team_idx}) "
            "> div:nth-child(1) > strong > a",
            first=True,
        )

        return team_anchor.text, team_anchor.attrs["href"].split("/")[2]

    def _parse_game_meta_data(self, html: Response) -> Tuple[datetime, str]:
        """
        Provided the BR game page it parses out the game time and
        game arena name.
        :return: Tuple(time of game start, name of the arena)
        """

        meta_holder = html.html.find("div.scorebox_meta", first=True)
        game_time = datetime.strptime(
            meta_holder.find("div")[1].text, "%I:%M %p, %B %d, %Y"
        )
        arena_name = meta_holder.find("div")[2].text.split(",")[0]

        return game_time, arena_name

    def _parse_attendance(self, html: Response) -> Optional[int]:
        """
        Provided the BR game page it parses out the game attendance.
        Sometimes the page doesn't include attendance in which case the
        method return None.
        :return: attendance as an integer
        """

        if "Attendance" not in html.text:
            return None

        attendance_text = html.text[
            html.text.index("Attendance") : html.text.index("Attendance") + 35
        ]

        digits = [s for s in attendance_text if s.isdigit()]

        return int("".join(digits))

    def _parse_game_id(self, game_url: str) -> str:
        """
        Provided a BR game url it parses out the game id.
        :return: game id as a string.
        """

        return (
            parse.urlsplit(game_url).path.split("/")[-1].replace(".html", "")
        )

    def _parse_basic_stats(
        self, page: Response, team: str, team_sn: str
    ) -> Dict[str, Union[int, float]]:
        """
        Provided the BR game page it parses out the basic stats
        for either the home or the road team, depending on the
        passed parameter.
        :team: inidcates if it team is home or away
        :return: dictionary of basic stats
        """

        table_finder = f"#box-{team_sn.upper()}-game-basic"

        tb = self._simple_parse(page.html, table_finder, txt=False)
        tb_foot = self._simple_parse(tb, "tfoot", txt=False)

        game_dic = {
            f"{team}_fg": int(self._simple_parse(tb_foot, "td[data-stat=fg]")),
            f"{team}_fga": int(
                self._simple_parse(tb_foot, "td[data-stat=fga]")
            ),
            f"{team}_fg_pct": float(
                self._simple_parse(tb_foot, "td[data-stat=fg_pct]")
            ),
            f"{team}_fg3": int(
                self._simple_parse(tb_foot, "td[data-stat=fg3]")
            ),
            f"{team}_fg3a": int(
                self._simple_parse(tb_foot, "td[data-stat=fg3a]")
            ),
            f"{team}_fg3_pct": float(
                self._simple_parse(tb_foot, "td[data-stat=fg3_pct]")
            ),
            f"{team}_ft": int(self._simple_parse(tb_foot, "td[data-stat=ft]")),
            f"{team}_fta": int(
                self._simple_parse(tb_foot, "td[data-stat=fta]")
            ),
            f"{team}_ft_pct": float(
                self._simple_parse(tb_foot, "td[data-stat=ft_pct]")
            ),
            f"{team}_orb": int(
                self._simple_parse(tb_foot, "td[data-stat=orb]")
            ),
            f"{team}_drb": int(
                self._simple_parse(tb_foot, "td[data-stat=drb]")
            ),
            f"{team}_trb": int(
                self._simple_parse(tb_foot, "td[data-stat=trb]")
            ),
            f"{team}_ast": int(
                self._simple_parse(tb_foot, "td[data-stat=ast]")
            ),
            f"{team}_stl": int(
                self._simple_parse(tb_foot, "td[data-stat=stl]")
            ),
            f"{team}_blk": int(
                self._simple_parse(tb_foot, "td[data-stat=blk]")
            ),
            f"{team}_tov": int(
                self._simple_parse(tb_foot, "td[data-stat=tov]")
            ),
            f"{team}_pf": int(self._simple_parse(tb_foot, "td[data-stat=pf]")),
            f"{team}_pts": int(
                self._simple_parse(tb_foot, "td[data-stat=pts]")
            ),
        }

        return game_dic

    def _parse_advanced_stats(
        self, page: Response, team: str, team_sn: str
    ) -> Dict[str, Union[int, float]]:
        """
        Provided the BR game page it parses out the advanced stats
        for either the home or the road team, depending on the
        passed parameter.
        :team: inidcates if the team is home or away
        :return: dictionary of basic stats
        """

        table_finder = f"#box-{team_sn.upper()}-game-advanced"

        tb = self._simple_parse(page.html, table_finder, txt=False)
        tb_foot = self._simple_parse(tb, "tfoot", txt=False)

        game_dic = {
            f"{team}_ts_pct": float(
                self._simple_parse(tb_foot, "td[data-stat=ts_pct]")
            ),
            f"{team}_efg_pct": float(
                self._simple_parse(tb_foot, "td[data-stat=efg_pct]")
            ),
            f"{team}_fg3a_per_fga_pct": float(
                self._simple_parse(tb_foot, "td[data-stat=fg3a_per_fga_pct]")
            ),
            f"{team}_fta_per_fga_pct": float(
                self._simple_parse(tb_foot, "td[data-stat=fta_per_fga_pct]")
            ),
            f"{team}_orb_pct": float(
                self._simple_parse(tb_foot, "td[data-stat=orb_pct]")
            ),
            f"{team}_drb_pct": float(
                self._simple_parse(tb_foot, "td[data-stat=drb_pct]")
            ),
            f"{team}_trb_pct": float(
                self._simple_parse(tb_foot, "td[data-stat=trb_pct]")
            ),
            f"{team}_ast_pct": float(
                self._simple_parse(tb_foot, "td[data-stat=ast_pct]")
            ),
            f"{team}_stl_pct": float(
                self._simple_parse(tb_foot, "td[data-stat=stl_pct]")
            ),
            f"{team}_blk_pct": float(
                self._simple_parse(tb_foot, "td[data-stat=blk_pct]")
            ),
            f"{team}_tov_pct": float(
                self._simple_parse(tb_foot, "td[data-stat=tov_pct]")
            ),
            f"{team}_off_rtg": float(
                self._simple_parse(tb_foot, "td[data-stat=off_rtg]")
            ),
            f"{team}_def_rtg": float(
                self._simple_parse(tb_foot, "td[data-stat=def_rtg]")
            ),
        }

        return game_dic


if __name__ == "__main__":
    pass
