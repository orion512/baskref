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

    print(settings)
    print(f'I am collecting all games on this day: __')

    return {}


def run_team_collector():
    pass


def run_player_collector():
    pass


def run_season_games_collector(settings: Settings) -> Dict[str, List]:
    """ Integrates the data collection layer jobs together """

    settings.logger.info('Getting Started')

    YEAR = 2008

    br = BasketballReference()

    month_urls = br.scrape_all_months_urls(YEAR)
    settings.logger.info(f'Scraped {len(month_urls)} month urls')

    game_urls = br.scrape_multiple_game_url_pages(month_urls)
    settings.logger.info(f'Scraped {len(game_urls)} game urls')
    
    game_data = br.scrape_multiple_games_data(game_urls)
    settings.logger.info(f'Scraped {len(game_data)} games')

    import pandas as pd
    pd.DataFrame(game_data).to_csv('test.csv', index=False)


def run_playoffs_game_collector():
    pass


if __name__ == '__main__':
    pass
