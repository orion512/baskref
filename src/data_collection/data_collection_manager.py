"""
This is the maanger script which orchestrates the data collection.
It is agnostic to the method fo collection & source of the data:
    - scraping a website
    - api
    - another database

Author: Dominik Zulovec Sajovic, May 2022
"""

import logging

from typing import Dict, List

from settings.settings import Settings
from src.data_collection.basketball_reference.scraper import \
    BasketballReference


def run_data_collection_manager(
    settings: Settings,
    logger: logging.Logger) -> Dict[str, List]:
    """ Integrates the data collection layer jobs together """

    logger.info('Getting Started')

    YEAR = 2008

    br = BasketballReference()

    month_urls = br.scrape_all_months_urls(YEAR)
    logger.info(f'Scraped {len(month_urls)} month urls')

    game_urls = br.scrape_multiple_game_url_pages(month_urls)
    logger.info(f'Scraped {len(game_urls)} game urls')
    
    game_data = br.scrape_multiple_games_data(game_urls)
    logger.info(f'Scraped {len(game_data)} games')

    import pandas as pd
    pd.DataFrame(game_data).to_csv('test.csv', index=False)


if __name__ == '__main__':
    pass
