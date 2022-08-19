"""
This is the manager script which orchestrates the data saving.

Depending on the passed argument the data can get saved in:
- CSV (main functionality)
- PostgreSQL (optional later feature)

Author: Dominik Zulovec Sajovic, June 2022
"""


import os

from settings.settings import Settings
from src.utils.error_utils import IllegalArgumentError
from src.data_saving.file_saver.pandas_saver import save_file_from_list


def run_data_saver_manager(settings: Settings, coll_data: list) -> None:
    """..."""

    date_str = settings.in_line.date.strftime("%Y%m%d")
    file_name = f"{date_str}_{settings.in_line.type}.csv"

    if settings.in_line.save == "f":
        save_path = os.path.join(settings.in_line.file_path, file_name)
        save_file_from_list(coll_data, save_path)
        settings.logger.info(f"Saved the file to: {save_path}")
    elif settings.in_line.type == "db":
        # save_to_db()
        pass
    else:
        raise IllegalArgumentError(
            f"{settings.in_line.type} is not a valid value for the save ",
            "(-f) argument. Choose one of the following: f, db.",
        )
