"""
This is the maanger script which orchestrates the data collection.
It is agnostic to the method fo collection & source of the data:
    - scraping a website
    - api
    - another database

Author: Dominik Zulovec Sajovic, May 2022
"""

from src.data_collection.basketball_reference.scraper import \
    BasketballReference


def run_data_collection_manager():
    """ Integrates the data collection layer jobs together """

    YEAR = 2008

    br = BasketballReference()
    month_urls = br.scrape_all_months_urls(YEAR)
    game_urls = br.scrape_multiple_game_url_pages(month_urls)
    print(len(game_urls))
    # games = br.scrape_all_games_data(YEAR)
    # df_games = pd.DataFrame(games)

    # hours, rem = divmod(end-start, 3600)
    # minutes, seconds = divmod(rem, 60)
    # print(f"Scrape All Game URLs Execution Time: {int(hours):0>2}:{int(minutes):0>2}:{seconds:05.2f}")
        



if __name__ == '__main__':
    run_data_collection_manager()
