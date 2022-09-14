# BaskRef (Basketball Scraper)
BaskRef is a tool to scrape basketball Data from the web.

The goal of this project is to provide a data collection utility for 
NBA basketball data. The collection strategy is to scrape data from 
https://www.basketball-reference.com.
The data can then be saved into a csv to be used by a different utility.

## About the Package

### What data are we collecting?

- games & game stats (in depth stats of the games)
    - by day
    - by whole season (regular + playoffs)
    - by playoffs
- teams (Not Implemented)
- players (Not Implemented)
- game logs (Not Implemented)
- player stats (Not Implemented)

## How to Install & Run the Package?

Install the project
```bash
pip install baskref
```

Set logging level (optional)
```bash
# INFO, DEBUG, ERROR
export LOG_LEVEL=DEBUG
# if not set default value is INFO
```

Scrape all games for the 7th of January 2022.
```bash
baskref -t g -d 2022-01-07 -fp datasets
# if you don't install the package
python -c "from baskref import run_baskref; run_baskref()" -t g -d 2022-01-07 -fp datasets
```

Scrape all games for the 2006 NBA season (regular season + playoffs).
```bash
baskref -t gs -y 2006 -fp datasets
# if you don't install the package
python -c "from baskref import run_baskref; run_baskref()" -t gs -y 2006 -fp datasets
```

Scrape all games for the 2006 NBA playoffs.
```bash
baskref -t gp -y 2006 -fp datasets
# if you don't install the package
python -c "from baskref import run_baskref; run_baskref()" -t gp -y 2006 -fp datasets
```

## How to Use the Package?

Install requirements
```bash
pip install -r requirements.txt
```

### Data Collection Utility
This refers to the scraping functionalities.

For any mode of collection first you need to import the below classes.
```python
from baskref.data_collection import (
    BaskRefUrlScraper,
    BaskRefDataScraper,
)
```
The BaskRefDataScraper.get_games_data returns a list of dictionaries.

Collect games for a specific day
```python
from datetime import date

url_scraper = BaskRefUrlScraper()
game_urls = url_scraper.get_game_urls_day(date(2022,1,7))
data_scraper = BaskRefDataScraper()
game_data = data_scraper.get_games_data(game_urls)

url_scraper = BaskRefUrlScraper()
game_urls = url_scraper.get_game_urls_day(date(2022,1,7))
data_scraper = BaskRefDataScraper()
game_data = data_scraper.get_games_data(game_urls)
```

Collect games for a specific season (regular + playoffs)
```python
url_scraper = BaskRefUrlScraper()
game_urls = url_scraper.get_game_urls_year(2006)
data_scraper = BaskRefDataScraper()
game_data = data_scraper.get_games_data(game_urls)
```

Collect games for a specific postseason
```python
url_scraper = BaskRefUrlScraper()
game_urls = url_scraper.get_game_urls_playoffs(2006)
data_scraper = BaskRefDataScraper()
game_data = data_scraper.get_games_data(game_urls)
```

### Data Saving Package
This refers to the saving of the data.

Save a list of dictionaries to a CSV file.
```python
import os
from baskref.data_saving.file_saver import save_file_from_list

save_path = os.path.join('datasets', 'file_name.csv')
save_file_from_list(game_data, save_path)
```

## How to Run Tests?

Run all tests with Pytest
```
pytest
```

Run just the unit tests
```
pytest -v -m unittest
```

Run just the integration tests
```
pytest -v -m integrationtest
```

Run coverage
```
coverage run --source=baskref -m pytest
coverage report --omit="*/test*" -m --skip-empty
```

## Code Formating

The code base uses black for automatic formating.
the configuration for black is stored in pyproject.toml file.

```bash
# run black over the entire code base
black .
```

## Linting

The code base uses pylint and mypy for code linting.

### Pylint

the configuration for pylint is stored in .pylintrc file.

```bash 
# run pylint over the entire code base
pylint run.py
pylint settings
pylint src
pylint tests
```

### MyPy

the configuration for mypy is stored in pyproject.toml file.

```bash 
# run mypy over the entire code base
mypy .
```

## Bonus

**Virtual Environment (optional)**
You might want to use a virtual environment for executing the project.

Create a new virtual environemnt
```
python -m venv venv  # The second parameter is a path to the virtual env.
```

Activate the new virtual environment
```
# Windows
.\venv\Scripts\activate

# Unix
source venv/bin/activate
```

Leaving the virtual environment
```
deactivate
```

### Contributors

1. [Dominik Zulovec Sajovic](https://www.linkedin.com/in/dominik-zulovec-sajovic/)
