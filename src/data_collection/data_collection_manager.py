"""
This is the maanger script which orchestrates the data collection.
It is agnostic to the method fo collection & source of the data:
    - scraping a website
    - api
    - another database

Author: Dominik Zulovec Sajovic, May 2022
"""

from typing import Dict, List

from settings.settings import Settings
from src.data_collection.basketball_reference.scraper import \
    BasketballReference


def run_daily_game_collector(settings: Settings) -> dict:
    """
    This function orchestrates the collection of NBA games on
    a specific day.
    """

    settings.logger.info(f'DAILY GAME COLLECTOR MODE')
    settings.logger.info(f'Collecting all games for: {settings.in_line.date}')
    br = BasketballReference()

    # 1. Get all the game urls for the specific day
    game_urls = br.scrape_game_urls_day(settings.in_line.date)
    settings.logger.info(f'Scraped {len(game_urls)} game urls')

    # 2. Get the game data for the list of games
    game_data = br.scrape_multiple_games_data(game_urls)
    settings.logger.info(f'Scraped {len(game_data)} games')

    return game_data


def run_team_collector():
    pass


def run_player_collector():
    pass


def run_season_games_collector(settings: Settings) -> Dict[str, List]:
    """ Integrates the data collection layer jobs together """

    settings.logger.info(f'SEASON GAME COLLECTOR MODE')
    settings.logger.info(f'Collecting all games for: {settings.in_line.year}')
    br = BasketballReference()

    # 1. Get all the months in a specific season
    month_urls = br.scrape_all_months_urls(settings.in_line.year)
    settings.logger.info(f'Scraped {len(month_urls)} month urls')

    # 2. Get all the game urls for all months in a season
    game_urls = br.scrape_multiple_game_urls_month(month_urls)
    settings.logger.info(f'Scraped {len(game_urls)} game urls')
    
    # 3. Get the game data for the list of games
    game_data = br.scrape_multiple_games_data(game_urls)
    settings.logger.info(f'Scraped {len(game_data)} games')

    return game_data


def run_playoffs_game_collector():
    pass


if __name__ == '__main__':
    pass
