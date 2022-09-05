"""
Holds the tests for the basketball refernce scraper class

Author: Dominik Zulovec Sajovic - August 2022
"""

from datetime import date
import pytest
from src.data_collection.scraper import (
    BasketRefUrlScraper,
)

# pylint: disable=protected-access


class TestBasketRefUrlScraper:
    """Class for BasketRefUrlScraper class"""

    test_url_generation: list[tuple] = [
        (
            "https://www.basketball-reference.com",
            2019,
            "https://www.basketball-reference.com/leagues/NBA_2019_games.html",
        ),
        (
            "https://www.basketball-reference.com",
            1947,
            "https://www.basketball-reference.com/leagues/NBA_1947_games.html",
        ),
        (
            "www.basketball-reference.com",
            2000,
            "www.basketball-reference.com/leagues/NBA_2000_games.html",
        ),
        ("", 2010, "/leagues/NBA_2010_games.html"),
        (
            "https://hostname/",
            20100298382,
            "https://hostname//leagues/NBA_20100298382_games.html",
        ),
    ]

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "input_url, input_year, expected_status", test_url_generation
    )
    def test_generate_season_games_url_correct(
        self, input_url, input_year, expected_status
    ):
        """Tests the function generate_season_games_url."""

        br_scraper = BasketRefUrlScraper(input_url)

        returned_status = br_scraper._generate_season_games_url(input_year)
        assert expected_status == returned_status

    test_url_generation_raise: list[tuple] = [
        (None, None, pytest.raises(ValueError)),
        (1940, None, pytest.raises(ValueError)),
        (1946, None, pytest.raises(ValueError)),
        (-92, None, pytest.raises(ValueError)),
        ("2006", None, pytest.raises(ValueError)),
        ("2006", None, pytest.raises(ValueError)),
        (2006.3, None, pytest.raises(ValueError)),
    ]

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "input_year, expected_status, raise_err", test_url_generation_raise
    )
    def test_generate_season_games_url_raise(
        self, input_year, raise_err, expected_status
    ):
        """Tests the function generate_season_games_url."""

        br_scraper = BasketRefUrlScraper()

        with pytest.raises(raise_err.expected_exception):
            returned_status = br_scraper._generate_season_games_url(input_year)
            assert expected_status == returned_status

    test_game_urls: list[tuple] = [
        ("", date(2018, 7, 9), "/boxscores/?month=7&day=9&year=2018"),
        ("", date(2021, 12, 1), "/boxscores/?month=12&day=1&year=2021"),
        ("", date(2000, 1, 1), "/boxscores/?month=1&day=1&year=2000"),
        ("", date(1957, 9, 9), "/boxscores/?month=9&day=9&year=1957"),
    ]

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "input_url, game_date, expected_status", test_game_urls
    )
    def test_generate_daily_games_url_correct(
        self, input_url, game_date, expected_status
    ):
        """Tests the function scrape_game_urls_day."""

        br_scraper = BasketRefUrlScraper(input_url)

        returned_status = br_scraper._generate_daily_games_url(game_date)
        assert expected_status == returned_status

    test_game_urls_raise: list[tuple] = [
        ("2018-07-09", None, pytest.raises(ValueError)),
        ("1993/12/05", None, pytest.raises(ValueError)),
        (None, None, pytest.raises(ValueError)),
    ]

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "game_date, expected_status, raise_err", test_game_urls_raise
    )
    def test_generate_daily_games_url_raise(
        self, game_date, expected_status, raise_err
    ):
        """Tests the function scrape_game_urls_day."""

        br_scraper = BasketRefUrlScraper()

        with pytest.raises(raise_err.expected_exception):
            returned_status = br_scraper._generate_daily_games_url(game_date)
            assert expected_status == returned_status
