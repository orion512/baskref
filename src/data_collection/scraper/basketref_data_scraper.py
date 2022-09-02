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

from dataclasses import dataclass
from datetime import datetime
from typing import Tuple, Optional, Dict, Union
from urllib import parse
from requests_html import HTMLResponse
from src.data_collection.scraper import Scraper


@dataclass
class BasketRefDataScraper(Scraper):
    """Class for scraping & Parsing basketball-reference.com data"""

    # public functions

    def get_games_data(self, game_urls: list) -> list:
        """
        Scrapes the data for all the game urls provided
        :game_urls: list of box score game urls from basketball reference
        :return: returns a list of dictionaries with game data
        """

        return [self._scrape_game_data(url) for url in game_urls]

    # Private Methods

    ## scraping functions

    def _scrape_game_data(self, game_url: str) -> dict:
        """
        Scrapes the data for the given game web page.
        :game_url: a Basketball Reference URL to a game page
        :return: returns a dictionary of game data
        """

        game_data = self.scrape(game_url, self._parse_full_game_data)
        game_data["game_id"] = self._parse_game_id(game_url)
        game_data["game_url"] = game_url

        return game_data

    ## parsing functions

    def _parse_full_game_data(self, game_page: HTMLResponse) -> dict:
        """
        Scrapes the data for the given game web page.
        :game_url: a Basketball Reference URL to a game page
        :return: returns a dictionary of game data
        """

        # Team names
        home_team_fn, home_team_sn = self._parse_team_name(game_page, "home")
        away_team_fn, away_team_sn = self._parse_team_name(game_page, "away")

        # game meta data
        game_time, arena_name = self._parse_game_meta_data(game_page)
        attendance = self._parse_attendance(game_page)

        # basic stats
        home_basic_dic = self._parse_basic_stats(
            game_page, "home", home_team_sn
        )

        away_basic_dic = self._parse_basic_stats(
            game_page, "away", away_team_sn
        )

        # advanced stats
        home_advanced_dic = self._parse_advanced_stats(
            game_page, "home", home_team_sn
        )

        away_advanced_dic = self._parse_advanced_stats(
            game_page, "away", away_team_sn
        )

        return {
            "home_team": home_team_sn,
            "away_team": away_team_sn,
            "home_team_full_name": home_team_fn,
            "away_team_full_name": away_team_fn,
            "game_time": game_time,
            "arena_name": arena_name,
            "attendance": attendance,
            **home_basic_dic,
            **away_basic_dic,
            **home_advanced_dic,
            **away_advanced_dic,
        }

    def _parse_team_name(
        self, html: HTMLResponse, team: str
    ) -> Tuple[str, str]:
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

    def _parse_game_meta_data(
        self, html: HTMLResponse
    ) -> Tuple[datetime, str]:
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

    def _parse_attendance(self, html: HTMLResponse) -> Optional[int]:
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
        self, page: HTMLResponse, team: str, team_sn: str
    ) -> Dict[str, Union[int, float]]:
        """
        Provided the BR game page it parses out the basic stats
        for either the home or the road team, depending on the
        passed parameter.
        :team: inidcates if it team is home or away
        :return: dictionary of basic stats
        """

        table_finder = f"#box-{team_sn.upper()}-game-basic"

        table = self.simple_parse(page.html, table_finder, txt=False)
        tb_foot = self.simple_parse(table, "tfoot", txt=False)

        game_dic = {
            f"{team}_fg": int(self.simple_parse(tb_foot, "td[data-stat=fg]")),
            f"{team}_fga": int(
                self.simple_parse(tb_foot, "td[data-stat=fga]")
            ),
            f"{team}_fg_pct": float(
                self.simple_parse(tb_foot, "td[data-stat=fg_pct]")
            ),
            f"{team}_fg3": int(
                self.simple_parse(tb_foot, "td[data-stat=fg3]")
            ),
            f"{team}_fg3a": int(
                self.simple_parse(tb_foot, "td[data-stat=fg3a]")
            ),
            f"{team}_fg3_pct": float(
                self.simple_parse(tb_foot, "td[data-stat=fg3_pct]")
            ),
            f"{team}_ft": int(self.simple_parse(tb_foot, "td[data-stat=ft]")),
            f"{team}_fta": int(
                self.simple_parse(tb_foot, "td[data-stat=fta]")
            ),
            f"{team}_ft_pct": float(
                self.simple_parse(tb_foot, "td[data-stat=ft_pct]")
            ),
            f"{team}_orb": int(
                self.simple_parse(tb_foot, "td[data-stat=orb]")
            ),
            f"{team}_drb": int(
                self.simple_parse(tb_foot, "td[data-stat=drb]")
            ),
            f"{team}_trb": int(
                self.simple_parse(tb_foot, "td[data-stat=trb]")
            ),
            f"{team}_ast": int(
                self.simple_parse(tb_foot, "td[data-stat=ast]")
            ),
            f"{team}_stl": int(
                self.simple_parse(tb_foot, "td[data-stat=stl]")
            ),
            f"{team}_blk": int(
                self.simple_parse(tb_foot, "td[data-stat=blk]")
            ),
            f"{team}_tov": int(
                self.simple_parse(tb_foot, "td[data-stat=tov]")
            ),
            f"{team}_pf": int(self.simple_parse(tb_foot, "td[data-stat=pf]")),
            f"{team}_pts": int(
                self.simple_parse(tb_foot, "td[data-stat=pts]")
            ),
        }

        return game_dic

    def _parse_advanced_stats(
        self, page: HTMLResponse, team: str, team_sn: str
    ) -> Dict[str, Union[int, float]]:
        """
        Provided the BR game page it parses out the advanced stats
        for either the home or the road team, depending on the
        passed parameter.
        :team: inidcates if the team is home or away
        :return: dictionary of basic stats
        """

        table_finder = f"#box-{team_sn.upper()}-game-advanced"

        table = self.simple_parse(page.html, table_finder, txt=False)
        tb_foot = self.simple_parse(table, "tfoot", txt=False)

        game_dic = {
            f"{team}_ts_pct": float(
                self.simple_parse(tb_foot, "td[data-stat=ts_pct]")
            ),
            f"{team}_efg_pct": float(
                self.simple_parse(tb_foot, "td[data-stat=efg_pct]")
            ),
            f"{team}_fg3a_per_fga_pct": float(
                self.simple_parse(tb_foot, "td[data-stat=fg3a_per_fga_pct]")
            ),
            f"{team}_fta_per_fga_pct": float(
                self.simple_parse(tb_foot, "td[data-stat=fta_per_fga_pct]")
            ),
            f"{team}_orb_pct": float(
                self.simple_parse(tb_foot, "td[data-stat=orb_pct]")
            ),
            f"{team}_drb_pct": float(
                self.simple_parse(tb_foot, "td[data-stat=drb_pct]")
            ),
            f"{team}_trb_pct": float(
                self.simple_parse(tb_foot, "td[data-stat=trb_pct]")
            ),
            f"{team}_ast_pct": float(
                self.simple_parse(tb_foot, "td[data-stat=ast_pct]")
            ),
            f"{team}_stl_pct": float(
                self.simple_parse(tb_foot, "td[data-stat=stl_pct]")
            ),
            f"{team}_blk_pct": float(
                self.simple_parse(tb_foot, "td[data-stat=blk_pct]")
            ),
            f"{team}_tov_pct": float(
                self.simple_parse(tb_foot, "td[data-stat=tov_pct]")
            ),
            f"{team}_off_rtg": float(
                self.simple_parse(tb_foot, "td[data-stat=off_rtg]")
            ),
            f"{team}_def_rtg": float(
                self.simple_parse(tb_foot, "td[data-stat=def_rtg]")
            ),
        }

        return game_dic
