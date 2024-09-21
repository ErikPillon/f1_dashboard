import fastf1 as ff1
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os
from pathlib import Path
from orm import Base, LapData, Drivers, Races
from dataclasses import dataclass

load_dotenv()
cache = ff1.Cache.enable_cache(".venv")

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

# Create a metadata instance
metadata = MetaData()

# Bind the engine to the metadata
metadata.bind = engine

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

LapData.__table__.create(engine, checkfirst=True)

directory_of_this_file = Path(__file__).parent


def fetch_data(year, gp):
    with engine.connect() as connection:
        connection.execute("SET search_path TO 1")


def get_quali_data(year, gp):
    quali = ff1.get_session(year, gp, "Q")
    return quali


def get_race_id(year: int, gp: int):
    """return the raceId for the given `year` and `gp`

    Args:
        year (int): GP year
        gp (int): GP round
    """
    pass


def get_driver_id(code: str, forename: str = None, surname: str = None):
    """return the driverId for the given `code`, `forename` and `surname`;
    `forename` and `surname` are optional and used only is not possible to uniquely
    identify the driver with its code.

    Args:
        code (str): driver code
        forename (str, optional): _description_. Defaults to None.
        surname (str, optional): _description_. Defaults to None.
    """
    pass


def quali_data_exists(year: int, gp: int):
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


# def fetch_driverId(code, forename, surname):
#     query = f"""
#         SELECT
#             driverId
#         FROM
#             drivers
#         WHERE
#             code = '{code}';
#         """

#     data = fetch_data_from_query(engine, query)

#     if len(data) != 1:
#         query = f"""
#         SELECT
#             driverId
#         FROM
#             drivers
#         WHERE
#             code = '{code}'
#             AND forename = '{forename}'
#             AND surname = '{surname}';
#         """
#     return fetch_data_from_query(engine, query)


def table_exists(table_name):
    query = f"""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = '{table_name}'
        );
        """

    return False


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


def create_table():
    Base.metadata.create_all(engine, tables=[LapData.__table__])


def create_lap_data_objects(df, driverId: int, raceId: int):
    lap_data_objects = []

    for _, row in df.iterrows():
        row["Time"] = (
            str(row["Time"]).split()[2]
            if isinstance(row["Time"], pd.Timedelta)
            else row["Time"]
        )
        lap_data_object = LapData(
            driverId=driverId,
            raceId=raceId,
            Time=row["Time"],
            RPM=row["RPM"],
            Speed=row["Speed"],
            nGear=row["nGear"],
            Throttle=row["Throttle"],
            Brake=row["Brake"],
            DRS=row["DRS"],
            Source=row["Source"],
            RelativeDistance=row["RelativeDistance"],
            Status=row["Status"],
            X=row["X"],
            Y=row["Y"],
            Z=row["Z"],
            Distance=row["Distance"],
        )
        lap_data_objects.append(lap_data_object)
    return lap_data_objects


def data_exists(driver_id: int, race_id: int):
    return (
        session.query(LapData).filter_by(driverId=driver_id, raceId=race_id).first()
        is not None
    )


def main():
    year = 2024
    gp = 1
    quali = ff1.get_session(2024, 1, "Q")
    quali.load()

    drivers = quali.laps.Driver.unique()
    for driver in drivers:
        laps = quali.laps.pick_driver(driver)
        # Select the fastest lap
        fastest = laps.pick_fastest()
        telemetry = fastest.get_telemetry().add_distance()

        race_id = session.query(Races).filter_by(year=year, round=gp).first().raceId
        driver_id = session.query(Drivers).filter_by(code=driver).first().driverId

        if not data_exists(driver_id, race_id):
            lapData_objects = create_lap_data_objects(telemetry, driver_id, race_id)
            session.add_all(lapData_objects)
            session.commit()
            print("added data for driver {} and race {}".format(driver_id, race_id))
        else:
            print(
                "data already present in the db for driver {} and race {}".format(
                    driver_id, race_id
                )
            )
    # if not data_exists(year=year, gp=gp):
    #     # retrievale of the data
    #     data = get_quali_data(year, gp)
    #     data.load()
    #     save_retrieved_data(data.laps, "quali", year, gp)

    # data = load_data(year, gp)
    # print(data.head())
    # breakpoint()

    # load_data_into_db(data)

    # pass


if __name__ == "__main__":
    main()
    # data = Driver(code="HAM")
    # print(data)
