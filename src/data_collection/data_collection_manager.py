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
    # month_urls = br.scrape_all_months_urls(YEAR)
    # game_urls = br.scrape_multiple_game_url_pages(month_urls)
    # logger.info(game_urls)

    test_url = 'https://www.basketball-reference.com/boxscores/200805160UTA.html'
    game_data = br.scrape_game_data(test_url)
    logger.info(game_data)
    
    # games = br.scrape_all_games_data(YEAR)
    # df_games = pd.DataFrame(games)

    # hours, rem = divmod(end-start, 3600)
    # minutes, seconds = divmod(rem, 60)
    # print(f"Scrape All Game URLs Execution Time: {int(hours):0>2}:{int(minutes):0>2}:{seconds:05.2f}")
        



if __name__ == '__main__':
    pass
