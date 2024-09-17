import fastf1 as ff1
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
import os
from dataclasses import dataclass

load_dotenv()
cache = ff1.Cache.enable_cache(".venv")

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


def fetch_data(year, gp):
    with engine.connect() as connection:
        connection.execute("SET search_path TO 1")


def get_quali_data(year, gp):
    quali = ff1.get_session(year, gp, "Q")
    return quali


def data_exists(year: int, gp: int):
    """check if the data for the given `year` and `gp` already exists"""

    return os.path.exists(f"retrieved_data/{year}/{gp}/quali.csv")


def save_retrieved_data(data: pd.DataFrame, data_type: str, year: int, gp_id: int):
    """save the data into a csv file

    Args:
        data (pd.DataFrame): _description_
        data_type (str): _description_
        year (int): the year of the data
        gp_id (int): the gp id of the data
    """
    path = f"retrieved_data/{year}/{gp_id}/"
    os.makedirs(path, exist_ok=True)
    data.to_csv(path + data_type + ".csv", index=False)


def load_data(year, gp):
    path = f"retrieved_data/{year}/{gp}/"
    return pd.read_csv(path + "quali.csv")


def fetch_driverId(code, forename, surname):
    query = f"""
        SELECT 
            driverId 
        FROM 
            drivers 
        WHERE 
            code = '{code}';
        """

    data = fetch_data_from_query(engine, query)

    if len(data) != 1:
        query = f"""
        SELECT 
            driverId 
        FROM 
            drivers 
        WHERE 
            code = '{code}' 
            AND forename = '{forename}' 
            AND surname = '{surname}';
        """
    return fetch_data_from_query(engine, query)


def insert_lap_data_into_db(
    driver_id,
    race_id,
    Time,
    RPM,
    Speed,
    nGear,
    Throttle,
    Brake,
    DRS,
    Source,
    RelativeDistance,
    Status,
    X,
    Y,
    Z,
    Distance,
):
    query = f"""
        INSERT INTO qualiLapTimes()
        VALUES ({driver_id}, {race_id}, {Time}, {RPM}, {Speed}, {nGear}, {Throttle}, {Brake}, {DRS}, {Source}, {RelativeDistance}, {Status}, {X}, {Y}, {Z}, {Distance});
        """


def table_exists(table_name):
    query = f"""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = '{table_name}'
        );
        """

    return fetch_data_from_query(engine, query)


@dataclass
class Driver:
    code: str
    forename: str
    surname: str
    _driverId: int = None

    def __post_init__(self):
        self.set_driverId(self._driverId)

    def set_driverId(self):
        self._driverId = fetch_driverId(
            code=self.code, forename=self.forename, surname=self.surname
        )


class GP:
    def __init__(self, year, gp):
        self.year = year
        self.gp = gp


def main():
    year = 2024
    gp = 1

    if not data_exists(year=year, gp=gp):
        # retrievale of the data
        data = get_quali_data(year, gp)
        data.load()
        save_retrieved_data(data.laps, "quali", year, gp)

    data = load_data(year, gp)

    if not table_exists("qualiLapTimes"):
        create_table()

    load_data_into_db(data)

    pass


if __name__ == "__main__":
    # main()
    data = Driver(code="HAM")
    print(data)
