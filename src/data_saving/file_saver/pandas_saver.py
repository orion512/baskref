"""
This script contains the functions required for pandas file saving.

Author: Dominik Zulovec Sajovic, June 2022
"""


import pandas as pd


def save_file_from_list(data: list, filepath: str) -> None:
    """ Saves a list of dictionaries as a CSV """
    pd.DataFrame(data).to_csv(filepath, index=False)
