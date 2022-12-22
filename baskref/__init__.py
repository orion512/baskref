"""
Imports all teh functions from the files in this package

Author: Dominik Zulovec Sajovic - August 2022
"""

import sys
import os
import argparse
import logging
from typing import Callable
from datetime import date

from baskref.settings import Settings, InLine
from baskref.utils import valid_date
from baskref.exceptions import IllegalArgumentError

from baskref.data_collection import (
    BaskRefUrlScraper,
    BaskRefDataScraper,
)
from baskref.data_collection.html_scraper import (
    TooManyRequests,
    PermissionDenied,
    ScrapingError,
)

from baskref.data_saving.file_saver import save_file_from_list

logger = logging.getLogger(__name__)


def run_baskref() -> None:
    """Entry point script which runs baskref"""

    logging.basicConfig(
        stream=sys.stdout,
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="""[%(asctime)s]\t%(levelname)s\t"""
        """%(name)s:%(lineno)d\t%(message)s""",
    )

    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

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
            gu - for game by date (only urls),
            gpl - player stats by date,
            gs - for all games in a year,
            gsu - for all games in a year (only urls),
            gspl - player stats all games in a year,
            gp - for all playoff games in a year,
            gpu - for all playoff games in a year (only urls)
            gppl - player stats playoff games in a year
        )
        """,
        choices=["g", "gu", "gpl", "gs", "gsu", "gspl", "gp", "gpu", "gppl"],
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

    parser.add_argument(
        "-p",
        "--proxy",
        help="""
        This parameter specifies the proxy to be used when sending requests.
        """,
        default=None,
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
        proxy=args.proxy,
    )

    settings = Settings(in_line=in_line)

    # 1. Run the data collection
    try:
        collected = run_data_collection_manager(settings)
    except TooManyRequests as exp:
        logger.info(
            ":( Server responded with an error due to too many requests. "
            "Try using a proxy or waiting at least 1 hour before continuing."
        )
        logger.debug(exp)
        sys.exit(1)
    except PermissionDenied as exp:
        logger.info(
            ":( Server responded with a permission error. "
            "Try using a proxy or different combination of user agents.",
        )
        logger.debug(exp)
        sys.exit(1)
    except ScrapingError as exp:
        logger.info(":( Server responded with an unexpected error.")
        logger.debug(exp)
        sys.exit(1)

    # 2. Run the data saver
    run_data_saving_manager(settings, collected)


## Data Collection Functions


def run_data_collection_manager(settings: Settings) -> list:
    """This function runs the selected mode of collection"""

    logger.info("Started the data collection manager")

    collection_modes: dict[str, Callable] = {
        "g": run_daily_collector,
        "gu": run_daily_collector,
        "gpl": run_daily_collector,
        "gs": run_season_collector,
        "gsu": run_season_collector,
        "gspl": run_season_collector,
        "gp": run_playoffs_collector,
        "gpu": run_playoffs_collector,
        "gppl": run_playoffs_collector,
    }

    if settings.in_line.type not in collection_modes:
        raise IllegalArgumentError(
            f"{settings.in_line.type} is not a valid value for the type ",
            "(-t) argument.",
        )

    return collection_modes[settings.in_line.type](settings)


def run_daily_collector(settings: Settings) -> list:
    """
    This function orchestrates the collection of data from NBA games on
    a specific day.
    """

    logger.info("DAILY GAME COLLECTOR MODE")
    logger.info(f"Collecting all game urls for: {settings.in_line.date}")

    # 1. Get all the game urls for the specific day
    url_scraper = BaskRefUrlScraper(settings.in_line.proxy)
    game_urls = url_scraper.get_game_urls_day(settings.in_line.date)
    logger.info(f"Scraped {len(game_urls)} game urls")

    if settings.in_line.type == "gu":
        return [{"url": url} for url in game_urls]

    # 2. Get the game data for the list of games
    data_scraper = BaskRefDataScraper(settings.in_line.proxy)

    if settings.in_line.type == "gpl":
        data = data_scraper.get_player_stats_data(game_urls)
    elif settings.in_line.type == "g":
        data = data_scraper.get_games_data(game_urls)

    logger.info(f"Scraped {len(data)} data points")

    return data


def run_season_collector(settings: Settings) -> list:
    """Orchestrates the collection of data in all games of a season"""

    logger.info("SEASON GAME COLLECTOR MODE")
    logger.info(f"Collecting all games for: {settings.in_line.year}")

    # 1. Get all the game urls for the specific year
    url_scraper = BaskRefUrlScraper(settings.in_line.proxy)
    game_urls = url_scraper.get_game_urls_year(settings.in_line.year)
    logger.info(f"Scraped {len(game_urls)} game urls")

    if settings.in_line.type == "gsu":
        return [{"url": url} for url in game_urls]

    # 2. Get the game data for the list of games
    data_scraper = BaskRefDataScraper(settings.in_line.proxy)

    if settings.in_line.type == "gspl":
        data = data_scraper.get_player_stats_data(game_urls)
    elif settings.in_line.type == "gs":
        data = data_scraper.get_games_data(game_urls)

    logger.info(f"Scraped {len(data)} data points")

    return data


def run_playoffs_collector(settings: Settings) -> list:
    """Orchestrates the collection of data in all games in a playoff"""

    logger.info("PLAYOFF GAME COLLECTOR MODE")
    logger.info(f"Collecting all games for: {settings.in_line.year} playoffs")

    # 1. Get all the game urls for the specific postseason
    url_scraper = BaskRefUrlScraper(settings.in_line.proxy)
    game_urls = url_scraper.get_game_urls_playoffs(settings.in_line.year)
    logger.info(f"Scraped {len(game_urls)} game urls")

    if settings.in_line.type == "gpu":
        return [{"url": url} for url in game_urls]

    # 2. Get the game data for the list of games
    data_scraper = BaskRefDataScraper(settings.in_line.proxy)

    if settings.in_line.type == "gppl":
        data = data_scraper.get_player_stats_data(game_urls)
    elif settings.in_line.type == "gp":
        data = data_scraper.get_games_data(game_urls)

    logger.info(f"Scraped {len(data)} data points")

    return data


## Data Saving Functions


def run_data_saving_manager(settings: Settings, coll_data: list) -> None:
    """Integration function which runs the saving of the data"""

    saving_prefix_options: dict[str, str] = {
        "g": settings.in_line.date.strftime("%Y%m%d"),
        "gu": settings.in_line.date.strftime("%Y%m%d"),
        "gpl": settings.in_line.date.strftime("%Y%m%d"),
        "gs": str(settings.in_line.year),
        "gsu": str(settings.in_line.year),
        "gspl": str(settings.in_line.year),
        "gp": str(settings.in_line.year),
        "gpu": str(settings.in_line.year),
        "gppl": str(settings.in_line.year),
    }

    chosen_prefix = saving_prefix_options[settings.in_line.type]
    file_name = f"{chosen_prefix}_{settings.in_line.type}.csv"

    save_path = os.path.join(settings.in_line.file_path, file_name)
    save_file_from_list(coll_data, save_path)
    logger.info(f"Saved the file to: {save_path}")
