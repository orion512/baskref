"""
This is the manager script which orchestrates the data collection.

This script is meant to have several modes of running.
- Daily scrape
- Yearly scrape
- Yearly Playoff scrape
- teams scrape
- players scrape
- (potentially in the future) date range scrape

type of scraping -t
    g -> to scrape daily games (-d for date)
    t -> to scrape all teams
    p -> to scrape all players (-n for last name char)
    gs -> to scrape all games in a year (-y for year)
    gp -> to scrape all playoff games in a year (-y for year)

Author: Dominik Zulovec Sajovic, May 2022
"""

from typing import List

from src.utils.error_utils import IllegalArgumentError
from settings.settings import Settings
from src.data_collection.basketball_reference.scraper import (
    BasketballReference,
)


def run_data_collection_manager(settings: Settings) -> List:
    """..."""

    if settings.in_line.type == "g":
        return run_daily_game_collector(settings)
    elif settings.in_line.type == "t":
        return run_team_collector(settings)
    elif settings.in_line.type == "p":
        return run_player_collector(settings)
    elif settings.in_line.type == "gs":
        return run_season_games_collector(settings)
    elif settings.in_line.type == "gp":
        return run_playoffs_game_collector(settings)
    else:
        raise IllegalArgumentError(
            f"{settings.in_line.type} is not a valid value for the type ",
            "(-t) argument. Choose one of the following: g, t, p, gs, gp.",
        )


def run_daily_game_collector(settings: Settings) -> List:
    """
    This function orchestrates the collection of NBA games on
    a specific day.
    """

    settings.logger.info("DAILY GAME COLLECTOR MODE")
    settings.logger.info(f"Collecting all games for: {settings.in_line.date}")
    br = BasketballReference()

    # 1. Get all the game urls for the specific day
    game_urls = br.scrape_game_urls_day(settings.in_line.date)
    settings.logger.info(f"Scraped {len(game_urls)} game urls")

    # 2. Get the game data for the list of games
    game_data = br.scrape_multiple_games_data(game_urls)
    settings.logger.info(f"Scraped {len(game_data)} games")

    return game_data


def run_team_collector():
    pass


def run_player_collector():
    pass


def run_season_games_collector(settings: Settings) -> List:
    """Orchestrates the collection of all games in a season"""

    settings.logger.info("SEASON GAME COLLECTOR MODE")
    settings.logger.info(f"Collecting all games for: {settings.in_line.year}")
    br = BasketballReference()

    # 1. Get all the months in a specific season
    month_urls = br.scrape_all_months_urls(settings.in_line.year)
    settings.logger.info(f"Scraped {len(month_urls)} month urls")

    # 2. Get all the game urls for all months in a season
    game_urls = br.scrape_multiple_game_urls_month(month_urls)
    settings.logger.info(f"Scraped {len(game_urls)} game urls")

    # 3. Get the game data for the list of games
    game_data = br.scrape_multiple_games_data(game_urls)
    settings.logger.info(f"Scraped {len(game_data)} games")

    return game_data


def run_playoffs_game_collector():
    pass


if __name__ == "__main__":
    pass
