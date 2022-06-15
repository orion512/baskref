"""
This is the manager script which orchestrates the data saving.

Depending on the passed argument the data can get saved in:
- CSV
- PostgreSQL
- SQLite

Author: Dominik Zulovec Sajovic, June 2022
"""

from typing import Dict, List

from src.utils.error_utils import IllegalArgumentError
from settings.settings import Settings
from src.data_saving.file_saver.pandas_saver import save_file_from_list


def run_data_saver_manager(settings: Settings, coll_data: list) -> None:
    """ ... """

    save_file_from_list(coll_data, 'C:\\Users\\Meltem\\Desktop\\test.csv')

    # if settings.in_line.type == 'f':
    #     # save_to_file
    #     pass
    # elif settings.in_line.type == 'db':
    #     # save_to_db()
    #     pass
    # else:
    #     raise IllegalArgumentError(
    #         f'{settings.in_line.type} is not a valid value for the type ',
    #         f'(-t) argument. Choose one of the following: g, t, p, gs, gp.'
    #         )