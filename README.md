# Basketball Scraper

The goal of this project is to set-up a basketball (NBA) database and fill it with data.
To go about this we implement include a few layers:
- DB Setup
    - Used to setup and manage the database 
- Data Collection Layer
    - Logic for pulling the data from an external data source
- ETL Manager
    - Calls the data collection layer and saves it into the database

## How to Setup?

### Install PostgreSQL DB (optional)
Install PostgreSQL for your operating system.
https://www.postgresql.org/download/

If you don't want to install a postgreSQL DB you can also choose to
save the data to flat files (CSV).

### Virtual Environment
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


## How to Run Tests?

## Project Structure

### DB Setup
- Tables:
    - team
    - player
    - game
    - player_game_stats

### Data Collection Layer

#### What data are we collecting?
- teams
- players
- game logs
- player stats

### ETL Manager

## Linting

check libraries to add to flake8
https://github.com/DmytroLitvinov/awesome-flake8-extensions#naming

```
mypy --ignore-missing-imports .
```