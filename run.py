"""

"""

import os
import argparse
import logging
import sys

from settings.settings import Settings
from src.data_collection.data_collection_manager import \
    run_data_collection_manager

def main(settings: Settings):
    """ The main entry point into the project """

    logger = logging.getLogger('blogger')
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    run_data_collection_manager(settings, logger)


if __name__ == "__main__":

    my_parser = argparse.ArgumentParser()

    parser = argparse.ArgumentParser()
    default_path = os.path.join('settings', 'settings.py')
    parser.add_argument(
        '-s', '--settings', 
        help='Path to Settings YAML File', 
        default=default_path, type=str)
    args = parser.parse_args()

    main(args.settings)
