import pytest
from .fetcher import fetch_seasons_years, fetch_championship_gp, fetch_gp_laps
import pandas as pd
import pytest
import pandas as pd

# from fixtures import db_engine
from .fetcher import (
    fetch_data_from_query,
    fetch_cumulative_points_by_constructor,
    fetch_cumulative_points_by_driver,
)

import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


@pytest.fixture()
def db_engine():
    return create_engine(DATABASE_URL)


def test_fetch_data_from_query_is_dataframe(db_engine):
    query = "SELECT 1 FROM results LIMIT 1;"
    data = fetch_data_from_query(db_engine, query)
    assert isinstance(data, pd.DataFrame)


def test_fetch_data_from_query_is_not_none(db_engine):
    query = "SELECT 1 FROM results LIMIT 1;"
    data = fetch_data_from_query(db_engine, query)
    assert not data.empty


@pytest.mark.parametrize("year", [year for year in range(1955, 2025)])
def test_fetch_cumulative_points_by_constructor(year):
    data = fetch_cumulative_points_by_constructor(year=year)
    assert not data.empty


@pytest.mark.parametrize("year", [year for year in range(1955, 2025)])
def test_fetch_cumulative_points_by_driver(year):
    data = fetch_cumulative_points_by_driver(year=year)
    assert not data.empty


def test_fetch_seasons_years():
    """check that the number os seasons is the same as the current year - 1950 + 1"""
    data = fetch_seasons_years()
    current_year = pd.Timestamp.now().year
    assert len(data) == current_year - 1950 + 1


@pytest.mark.parametrize(
    "year,expected", [(2023, 22), (2022, 22), (2021, 22), (2020, 17)]
)
def test_fetch_championship_gp(year, expected):
    data = fetch_championship_gp(year=year)

    assert len(data) == expected


@pytest.mark.parametrize("year,round,expected", [(2024, 1, 1129)])
def test_fetch_gp_laps(year, round, expected):
    data = fetch_gp_laps(year=year, round=round)

    assert len(data) == expected
