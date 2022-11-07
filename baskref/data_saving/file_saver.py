"""
This script contains the functions required for pandas file saving.

Author: Dominik Zulovec Sajovic, June 2022
"""

import os
import csv


def save_file_from_list(data: list[dict], filepath: str) -> None:
    """
    Saves a list of dictionaries as a CSV.
    This used to be implemented with pandas
    pd.DataFrame(data).to_csv(filepath, index=False)
    """

    if len(data) == 0:
        return

    # check that we have a list of dictionaries
    if not isinstance(data, list):
        raise ValueError("The parameter data has to be a list")

    if not check_all_elements_dicts(data):
        raise ValueError(
            "All the elements of the parameter data have to be dictionaires"
        )

    # if path to file doesn't exist -> create it
    folder_path = os.path.dirname(filepath)
    if (not os.path.exists(folder_path)) and (folder_path != ""):
        os.makedirs(folder_path)

    with open(filepath, "w", newline="", encoding="UTF-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def check_all_elements_dicts(list_param: list) -> bool:
    """inspects if all elements of the list are dictionaries"""

    if not isinstance(list_param, list):
        raise ValueError("The parameter list_param has to be a list")

    non_dicts = [ele for ele in list_param if not isinstance(ele, dict)]

    return len(non_dicts) == 0
