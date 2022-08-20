# Basketball Scraper

The goal of this project is to provide a data collection utility for 
NBA basketball data. The data is then saved into a csv to be used by
a different utility.

An optional future upgrade to the project will be to allow to store the
data into a postgreSQL database directly.

## How to Setup?

### Environment

Make sure th environment has the pip package manager.
https://pip.pypa.io/en/stable/installation/

Install requirements
```bash
pip install -r requirements.txt
```

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

## How to Run?



Scrape all games for the 7th of January 2022.
```
python run.py -t g -d 2022-01-07 -fp datasets
```

#### What data are we collecting?
- teams
- players
- game logs
- player stats


## How to Run Tests?


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

### Contributors

1. Dominik Zulovec Sajovic
