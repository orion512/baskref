"""
Imports all teh functions from the files in this package

Author: Dominik Zulovec Sajovic - August 2022
"""

import os
import argparse
from typing import List, Callable, Dict
from datetime import date

from baskref.settings import Settings, InLine
from baskref.utils import valid_date
from baskref.exceptions import IllegalArgumentError

from baskref.data_collection import (
    BaskRefUrlScraper,
    BaskRefDataScraper,
)

from baskref.data_saving.file_saver import save_file_from_list


def run_baskref() -> None:
    """Entry point script which runs baskref"""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s",
        "--settings",
        help="Path to Settings YAML File",
        default=os.path.join("settings", "settings.yaml"),
        type=str,
    )

    parser.add_argument(
        "-t",
        "--type",
        help="""
        Specifcy type of scraping (
            g - for game by date,
            t - for all teams,
            p - for all players,
            gs - for all games in a year,
            gp - for all playoff games in a year
        )
        """,
        choices=["g", "t", "p", "gs", "gp"],
        default="g",
        type=str,
    )

    parser.add_argument(
        "-d",
        "--date",
        help="""
        If type of scraping is -g (game by date) then
        this parameter specifies the date.
        By default ir will be set to today.
        """,
        default=date.today().strftime("%Y-%m-%d"),
        type=valid_date,
    )

    parser.add_argument(
        "-n",
        "--namechar",
        help="""
        If type of scraping is p (players) then
        this parameter specifies the first letter
        of the last name to scrape.
        The script will scrape all players matching the criteria.
        If the parameter is set to all, then all characters will be scraped.
        By default the parameter is set to all.
        """,
        default="all",
        type=str,
    )

    parser.add_argument(
        "-y",
        "--year",
        help="""
        If type of scraping is (gs) or (gp) (games by season/playoffs) then
        this parameter specifies the year of the season/playoffs.
        The year needs to match the ending year of the season.
        Example 2005/06 -> 2006.
        By default it will be set to the current year.
        """,
        default=date.today().year,
        type=int,
    )

    parser.add_argument(
        "-fp",
        "--file_path",
        help="""
        This parameter specifies path where to save the file.
        By default it will be set to the root of the project.
        """,
        default="datasets",
        type=str,
    )

    parameters = parser.parse_args()

    main(parameters)


def main(args: argparse.Namespace) -> None:
    """Extension of the baskref entrypoint."""

    in_line = InLine(
        type=args.type,
        date=args.date,
        namechar=args.namechar,
        year=args.year,
        file_path=args.file_path,
    )

    settings = Settings(in_line=in_line)

    # 1. Run the data collection
    collected = run_data_collection_manager(settings)

    # 2. Run the data saver
    run_data_saving_manager(settings, collected)


## Data Collection Functions


def run_data_collection_manager(settings: Settings) -> List:
    """This function runs the selected mode of collection"""

    settings.logger.info("Started the data collection manager")

    collection_modes: Dict[str, Callable] = {
        "g": run_daily_game_collector,
        "t": run_team_collector,
        "p": run_player_collector,
        "gs": run_season_games_collector,
        "gp": run_playoffs_game_collector,
    }

    if settings.in_line.type not in collection_modes:
        raise IllegalArgumentError(
            f"{settings.in_line.type} is not a valid value for the type ",
            "(-t) argument. Choose one of the following: g, t, p, gs, gp.",
        )

    return collection_modes[settings.in_line.type](settings)


def run_daily_game_collector(settings: Settings) -> List:
    """
    This function orchestrates the collection of NBA games on
    a specific day.
    """

    settings.logger.info("DAILY GAME COLLECTOR MODE")
    settings.logger.info(f"Collecting all games for: {settings.in_line.date}")

    # 1. Get all the game urls for the specific day
    url_scraper = BaskRefUrlScraper()
    game_urls = url_scraper.get_game_urls_day(settings.in_line.date)
    settings.logger.info(f"Scraped {len(game_urls)} game urls")

    # 2. Get the game data for the list of games
    data_scraper = BaskRefDataScraper()
    game_data = data_scraper.get_games_data(game_urls)
    settings.logger.info(f"Scraped {len(game_data)} games")

    return game_data


def run_team_collector():
    """This function orchestrates the collection of all NBA teams"""
    raise NotImplementedError


def run_player_collector():
    """This function orchestrates the collection of all NBA players"""
    raise NotImplementedError


def run_season_games_collector(settings: Settings) -> List:
    """Orchestrates the collection of all games in a season"""

    settings.logger.info("SEASON GAME COLLECTOR MODE")
    settings.logger.info(f"Collecting all games for: {settings.in_line.year}")

    # 1. Get all the game urls for the specific year
    url_scraper = BaskRefUrlScraper()
    game_urls = url_scraper.get_game_urls_year(settings.in_line.year)
    settings.logger.info(f"Scraped {len(game_urls)} game urls")

    # 2. Get the game data for the list of games
    data_scraper = BaskRefDataScraper()
    game_data = data_scraper.get_games_data(game_urls)
    settings.logger.info(f"Scraped {len(game_data)} games")

    return game_data


def run_playoffs_game_collector(settings: Settings) -> List:
    """Orchestrates the collection of all games in a playoff"""

    settings.logger.info("PLAYOFF GAME COLLECTOR MODE")
    settings.logger.info(
        f"Collecting all games for: {settings.in_line.year} playoffs"
    )

    # 1. Get all the game urls for the specific postseason
    url_scraper = BaskRefUrlScraper()
    game_urls = url_scraper.get_game_urls_playoffs(settings.in_line.year)
    settings.logger.info(f"Scraped {len(game_urls)} game urls")

    # 2. Get the game data for the list of games
    data_scraper = BaskRefDataScraper()
    game_data = data_scraper.get_games_data(game_urls)
    settings.logger.info(f"Scraped {len(game_data)} games")

    return game_data


## Data Saving Functions


def run_data_saving_manager(settings: Settings, coll_data: list) -> None:
    """Integration function which runs the saving of the data"""

    saving_prefix_options: Dict[str, str] = {
        "g": settings.in_line.date.strftime("%Y%m%d"),
        "t": "teams",
        "p": settings.in_line.namechar,
        "gs": str(settings.in_line.year),
        "gp": str(settings.in_line.year),
    }

    chosen_prefix = saving_prefix_options[settings.in_line.type]
    file_name = f"{chosen_prefix}_{settings.in_line.type}.csv"

    save_path = os.path.join(settings.in_line.file_path, file_name)
    save_file_from_list(coll_data, save_path)
    settings.logger.info(f"Saved the file to: {save_path}")
