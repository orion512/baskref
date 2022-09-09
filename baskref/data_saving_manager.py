"""
This is the manager script which orchestrates the data saving.

Author: Dominik Zulovec Sajovic, June 2022
"""


import os
from typing import Dict

from baskref.shared_utils.settings_utils import Settings
from baskref.data_saving.file_saver import save_file_from_list


def run_data_saving_manager(settings: Settings, coll_data: list) -> None:
    """Integration function which runs the saving of the data"""

    saving_prefix_options: Dict[str, str] = {
        "g": settings.in_line.date.strftime("%Y%m%d"),
        "t": "teams",
        "p": settings.in_line.namechar,
        "gs": str(settings.in_line.year),
        "gp": str(settings.in_line.year),
    }

    chosen_prefix = saving_prefix_options[settings.in_line.type]
    file_name = f"{chosen_prefix}_{settings.in_line.type}.csv"

    save_path = os.path.join(settings.in_line.file_path, file_name)
    save_file_from_list(coll_data, save_path)
    settings.logger.info(f"Saved the file to: {save_path}")
