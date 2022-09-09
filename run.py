"""
This script is the main entrace to the project.

Author: Dominik Zulovec Sajovic, May 2022
"""

import os
import argparse

from datetime import date
from baskref.shared_utils.settings_utils import Settings, InLine
from baskref.shared_utils.date_utils import valid_date
from baskref import (
    run_data_collection_manager,
    run_data_saving_manager,
)


def main(args: argparse.Namespace) -> None:
    """The main entry point into the project."""

    in_line = InLine(
        type=args.type,
        date=args.date,
        namechar=args.namechar,
        year=args.year,
        file_path=args.file_path,
    )

    settings = Settings(in_line=in_line)

    # Run the main packages
    # # 1. Run the data collection
    collected = run_data_collection_manager(settings)

    # # 2. Run the data saver
    run_data_saving_manager(settings, collected)


if __name__ == "__main__":

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
