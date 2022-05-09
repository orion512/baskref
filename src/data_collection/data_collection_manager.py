"""


- Scrape all teams https://www.basketball-reference.com/teams/
- Scrape all players https://www.basketball-reference.com/players/
- Scrape all games in a year https://www.basketball-reference.com/leagues/NBA_2022_games-april.html
    - scrape all months
    - scrape all games including link to box scores
- Scrape all playoff games in a year https://www.basketball-reference.com/playoffs/NBA_2022_games.html

Author: Dominik Zulovec Sajovic, May 2022
"""

import pandas as pd
from src.data_collection.basketball_reference.scraper import BasketballReference


def run_data_collection_manager():
    """ Integrates the data collection layer jobs together """

    YEAR = 2008

    br = BasketballReference()
    games = br.scrape_all_games_data(YEAR)
    df_games = pd.DataFrame(games)




if __name__ == '__main__':
    pass
