# BaskRef (Basketball Scraper)
BaskRef is a tool to scrape basketball Data from the web.

The goal of this project is to provide a data collection utility for 
NBA basketball data. The collection strategy is to scrape data from 
https://www.basketball-reference.com.
The data can then be saved into a csv to be used by a different utility.

## About the Package

### What data are we collecting?

- games & game stats (in depth stats of the games)
- players game stats

All datasets are available to be collected:
- by day (all games in one day)
- by whole season (regular + playoffs)
- by playoffs

#### Future Collections (Not yet implemented)
- players meta data (Not Implemented)
- game logs (Not Implemented)


## How to Install & Run the Package?

### Install the project
```bash
pip install baskref

# optional set logging level. Default value is INFO
export LOG_LEVEL=DEBUG # INFO, DEBUG, ERROR
```

### Scrape Game Data

Scrape all games for the 7th of January 2022.
```bash
baskref -t g -d 2022-01-07 -fp datasets
# python -c "from baskref import run_baskref; run_baskref()" -t g -d 2022-01-07 -fp datasets
```

Scrape all games for the 2006 NBA season (regular season + playoffs).
```bash
baskref -t gs -y 2006 -fp datasets
# python -c "from baskref import run_baskref; run_baskref()" -t gs -y 2006 -fp datasets
```

Scrape all games for the 2006 NBA playoffs.
```bash
baskref -t gp -y 2006 -fp datasets
# if you don't install the package
# python -c "from baskref import run_baskref; run_baskref()" -t gp -y 2006 -fp datasets
```

### Scrape Game URLs only

```bash
# simply add "u" to any of the three scraping types:
# g -> gu, gs -> gsu, gp -> gpu
baskref -t gu -d 2022-01-07 -fp datasets
```

### Scrape Player Stats Data

```bash
# simply add "pl" to any of the three scraping types:
# g -> gpl, gs -> gspl, gp -> gppl
baskref -t gpl -d 2022-01-07 -fp datasets
```

### Scrape Using a Proxy
Use proxy for scraping.
```bash
baskref -t g -d 2022-01-07 -fp datasets -p http://someproxy.com
```


## How to Use the Package?

Install requirements
```bash
pip install -r requirements.txt
```

### Data Collection Utility
This refers to the scraping functionalities.

For any mode of collection first you need to import and initialize 
the below classes.
```python
from baskref.data_collection import (
    BaskRefUrlScraper,
    BaskRefDataScraper,
)

url_scraper = BaskRefUrlScraper()
data_scraper = BaskRefDataScraper()

# optionally you can set a proxy
proxy_url_scraper = BaskRefUrlScraper("http://someproxy.com")
proxy_data_scraper = BaskRefDataScraper("http://someproxy.com")
```
The BaskRefDataScraper.get_games_data returns a list of dictionaries.

Collect games for a specific day
```python
from datetime import date

game_urls = url_scraper.get_game_urls_day(date(2022,1,7))
game_data = data_scraper.get_games_data(game_urls)
```

Collect games for a specific season (regular + playoffs)
```python
game_urls = url_scraper.get_game_urls_year(2006)
game_data = data_scraper.get_games_data(game_urls)
```

Collect games for a specific postseason
```python
game_urls = url_scraper.get_game_urls_playoffs(2006)
game_data = data_scraper.get_games_data(game_urls)
```

Collect player stats for for a specific day
```python
from datetime import date

game_urls = url_scraper.get_game_urls_day(date(2022,1,7))
pl_stats_data = data_scraper.get_player_stats_data(game_urls)
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

Run all tests with coverage
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
pylint --recursive=y ./
```

### MyPy

the configuration for mypy is stored in pyproject.toml file.

```bash 
# run mypy over the entire code base
mypy baskref
```

## Bonus

### Prepare project for development

1. Create Virtual Environment

- You might want to use a virtual environment for executing the project.
- this is an optional step (if skipping go straight to step 2)

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

2. Install all the dev requirements

```
pip install -r requirements_dev.txt

# uninstall all packages Windows
pip freeze > unins && pip uninstall -y -r unins && del unins

# uninstall all packages linux
pip freeze | xargs pip uninstall -y
```

3. Install the pre-commit hook
```
pre-commit install
```

### Prepare a new Version
This section describes some of the steps when preparing a new baskref version.

- adjust the pyproject.toml file
    - version
    - dependencies
- install project locally and test it
```
python -m build
pip install .
```
- publish project to test.pypi
```
pip install --upgrade twine
twine upload --repository testpypi dist/*
# install from test.pypi
pip install --index-url https://test.pypi.org/simple/ baskref
```
- publish a new version
```
twine upload dist/*
```


## Contributors

1. [Dominik Zulovec Sajovic](https://www.linkedin.com/in/dominik-zulovec-sajovic/)
