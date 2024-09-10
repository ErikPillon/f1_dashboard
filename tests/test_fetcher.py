import pytest
import pandas as pd

# from fixtures import db_engine
from ..fetcher import (
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


def test_fetch_cumulative_points_by_constructor():
    for i in range(1955, 2025):
        data = fetch_cumulative_points_by_constructor(year=i)
        assert not data.empty


def test_fetch_cumulative_points_by_driver():
    for i in range(1955, 2025):
        data = fetch_cumulative_points_by_driver(year=i)
        assert not data.empty
