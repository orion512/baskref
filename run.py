"""

"""

import os
import argparse

from src.data_collection.data_collection_manager import \
    run_data_collection_manager

def main(settings):
    run_data_collection_manager()


if __name__ == "__main__":

    my_parser = argparse.ArgumentParser()
    my_parser.add_argument(
        'config_path',
        metavar='path',
        type=str,
        help='Path to config YAML file.')
    args = my_parser.parse_args()

    parser = argparse.ArgumentParser()
    default_path = os.path.join('settings', 'settings.py')
    parser.add_argument(
        '-s', '--settings', 
        help='Path to Settings YAML File', 
        default=default_path, type=str)
    args = parser.parse_args()

    main(args.settings)
