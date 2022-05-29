"""
This script is meant to have 2 modes of running.
- Daily scrape
- Yearly scrape
- (potentially in the future) date range scrape

Depending on the passed argument the data can get saved in:
- CSV
- PostgreSQL
- SQLite

type of scraping -t
    g -> to scrape daily games (-d for date)
    t -> to scrape all teams
    p -> to scrape all players (-n for last name char)
    gs -> to scrape all games in a year (-y for year)
    gp -> to scrape all playoff games in a year (-y for year)

Author: Dominik Zulovec Sajovic, May 2022
"""

import os
import argparse
import logging
import sys

from datetime import date
from src.utils.date_utils import valid_date
from src.data_collection.data_collection_manager import \
    run_data_collection_manager

def main(args: argparse.Namespace):
    """ The main entry point into the project """

    logger = logging.getLogger('blogger')
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # TODO: add if/else for run based on arguments

    run_data_collection_manager(args.settings, logger)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-s', '--settings', 
        help='Path to Settings YAML File', 
        default=os.path.join('settings', 'settings.py'),
        type=str
    )
    
    parser.add_argument(
        '-t', '--type', 
        help="""
        Specifcy type of scraping (
            g - for game by date,
            t - for all teams,
            p - for all players,
            gs - for all games in a year,
            gp - for all playoff games in a year
        )
        """,
        choices=['g', 't', 'p', 'gs', 'gp'],
        default='g',
        type=str
    )

    parser.add_argument(
        '-d', '--date', 
        help="""
        If type of scraping is -g (game by date) then
        this parameter specifies the date.
        By default ir will be set to today.
        """,
        default=date.today().strftime('%Y-%m-%d'),
        type=valid_date
    )

    parser.add_argument(
        '-n', '--namechar', 
        help="""
        If type of scraping is p (players) then 
        this parameter specifies the first letter 
        of the last name to scrape.
        The script will scrape all players matching the criteria.
        If the parameter is set to all, then all characters will be scraped.
        By default the parameter is set to all. 
        """,
        default='all',
        type=str
    )

    parser.add_argument(
        '-y', '--year', 
        help="""
        If type of scraping is (gs) or (gp) (games by season/playoffs) then
        this parameter specifies the year of the season/playoffs.
        The year needs to match the ending year of the season.
        Example 2005/06 -> 2006.
        By default it will be set to the current year.
        """, 
        default=date.today().year,
        type=int
    )

    # TODO: add arguments for saving preference (csv, pg db, sqlite)
    args = parser.parse_args()

    print(args)

    # main(args)
