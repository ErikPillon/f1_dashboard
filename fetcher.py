import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Get the database URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)


@st.cache_data
def fetch_cumulative_points_by_constructor(year: int = 2024):
    query = f"""
    SELECT 
        r.round,
        c.name,
        SUM(res.points) as race_points,
        SUM(SUM(res.points)) OVER (PARTITION BY c.name ORDER BY r.round) as cumulative_points
    FROM
        results res
    JOIN 
        constructors c ON res.constructorId = c.constructorId
    JOIN 
        races r ON r.raceId = res.raceId
    WHERE 
        r.year = {year}
    GROUP BY
        r.round, c.name
    ORDER BY 
        r.round, c.name;
    """
    return fetch_data_from_query(engine, query)


@st.cache_data
def fetch_cumulative_points_by_driver(year: int = 2024):
    query = f"""
    SELECT 
        r.round,
        d.code,
        SUM(res.points) OVER (PARTITION BY d.code ORDER BY r.round) as cumulative_points
    FROM
        results res
    JOIN 
        drivers d ON res.driverId = d.driverId
    JOIN 
        races r ON r.raceId = res.raceId
    WHERE 
        r.year = {year};
    """
    return fetch_data_from_query(engine, query)


def fetch_data_from_query(engine, query: str):
    with engine.connect() as connection:
        df = pd.read_sql(query, connection)
    return df
