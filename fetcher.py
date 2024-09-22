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
def fetch_drivers_by_year(year: int = 2024):
    query = f"""
    SELECT 
        drivers.code,
        constructors.name
    FROM 
        results 
    JOIN 
        drivers on drivers.`DriverId` = results.`driverId` 
    JOIN 
        constructors on results.`constructorId` = constructors.`constructorId` 
    join 
        races on races.`raceId` = results.`raceId` 
    where 
        races.year = {year};
    """
    return fetch_data_from_query(engine, query)


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


@st.cache_data
def fetch_seasons_years():
    query = """
    SELECT 
        DISTINCT(year) as year
    FROM 
        seasons
    ORDER BY
        year DESC;
    """
    return fetch_data_from_query(engine, query)


def fetch_championship_gp(year: int) -> pd.DataFrame:
    """given a year return the list of races"""
    query = f"""
    SELECT
        r.round as round,
        r.date as date,
        r.url as url,
        r.name as name,
        c.name as circuit,
        c.location as location,
        c.country as country
    FROM
        races r
    JOIN 
        circuits c ON r.circuitId = c.circuitId
    WHERE
        r.year = {year}
    """
    return fetch_data_from_query(engine, query)


@st.cache_data
def fetch_gp_laps(year: int, round: int) -> pd.DataFrame:
    """given a year and round return the list of races"""
    query = f"""
        SELECT 
            lt.lap, 
            lt.position, 
            lt.milliseconds, 
            d.code
        FROM 
            `lapTimes` lt 
        JOIN 
            drivers d on d.`driverId`=lt.`driverId` 
        JOIN 
            races r on r.`raceId` = lt.`raceId` 
        WHERE 
            r.year = {year} 
        AND 
            r.round = {round};
        """
    return fetch_data_from_query(engine, query)


@st.cache_data
def fetch_number_of_poles_by_driver():
    query = """SELECT q.driverId, d.forename, d.surname, COUNT(*) as numberPoles FROM qualifying q JOIN drivers d ON d.driverId = q.driverId WHERE q.position = 1 GROUP BY q.driverId ORDER BY numberPoles DESC;"""
    return fetch_data_from_query(engine, query)


@st.cache_data
def fetch_number_of_wins_by_driver():
    query = """select r.driverId, d.forename, d.surname, count(*) as numberWins from results r join drivers d on d.driverId = r.driverId where r.position = 1 GROUP BY r.driverId ORDER BY numberWins DESC;"""
    return fetch_data_from_query(engine, query)


@st.cache_data
def fetch_laps_led_by_driver(year: int = 2024):
    query = f"""
        WITH laps_led_per_driver_CTE AS (
        SELECT
            lt.driverId,
            COUNT(*) AS number
        FROM
            lapTimes lt
        WHERE lt.raceId IN (
            SELECT raceId
            FROM races r
            WHERE r.year = {year}
        )
        AND lt.position = 1
        GROUP BY lt.driverId
    )
    -- Query to get laps led per driver
    SELECT
        d.forename,
        d.surname,
        ll_cte.number
    FROM
        drivers d
        JOIN laps_led_per_driver_CTE ll_cte ON ll_cte.driverId = d.driverId
    ORDER BY
        ll_cte.number DESC;
    """
    return fetch_data_from_query(engine, query)


@st.cache_data
def fetch_fastest_laps_by_driver(year: int = 2024):
    query = f"""
        WITH fastest_laps_by_driver_CTE AS (
        SELECT
            lt.driverId,
            COUNT(*) AS number
        FROM
            lapTimes lt
        WHERE lt.raceId IN (
            SELECT raceId
            FROM races r
            WHERE r.year = {year}
        )
        AND lt.position = 1
        GROUP BY lt.driverId
    )
    -- Query to get fastest laps per driver
    SELECT
        d.forename,
        d.surname,
        ll_cte.number
    FROM
        drivers d
        JOIN fastest_laps_by_driver_CTE ll_cte ON ll_cte.driverId = d.driverId
    ORDER BY
        ll_cte.number DESC;
    """
    return fetch_data_from_query(engine, query)


@st.cache_data
def fetch_number_of_laps_completed_by_driver(year: int = 2024):
    query = f"""
    WITH laps_per_driver_CTE AS (
        SELECT 
            lt.driverId, 
            COUNT(*) AS number 
        FROM 
            lapTimes lt 
        WHERE lt.raceId IN (
            SELECT raceId 
            FROM races r 
            WHERE r.year = {year}
        ) 
        GROUP BY lt.driverId
    )

    -- Query to get total laps per driver
    SELECT 
        d.forename, 
        d.surname, 
        l_cte.number 
    FROM 
        drivers d 
        JOIN laps_per_driver_CTE l_cte ON l_cte.driverId = d.driverId 
    ORDER BY 
        l_cte.number DESC;"""
    return fetch_data_from_query(engine, query)


@st.cache_data
def fetch_number_of_world_titles_by_driver():
    return pd.DataFrame()


def fetch_data_from_query(engine, query: str) -> pd.DataFrame:
    with engine.connect() as connection:
        df = pd.read_sql(query, connection)
    return df
