from sqlalchemy import (
    Column,
    Integer,
    Float,
    Boolean,
    String,
    ForeignKey,
    Date,
    Time,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Races(Base):
    __tablename__ = "races"

    raceId = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False, default=0)
    round = Column(Integer, nullable=False)
    circuitId = Column(Integer, nullable=False, default=0)
    name = Column(String(255), nullable=False, default="")
    date = Column(Date, nullable=False, default="0000-00-00")
    time = Column(Time, nullable=True)
    url = Column(String(255), nullable=True)
    fp1_date = Column(Date, nullable=True)
    fp1_time = Column(Time, nullable=True)
    fp2_date = Column(Date, nullable=True)
    fp2_time = Column(Time, nullable=True)
    fp3_date = Column(Date, nullable=True)
    fp3_time = Column(Time, nullable=True)
    quali_date = Column(Date, nullable=True)
    quali_time = Column(Time, nullable=True)
    sprint_date = Column(Date, nullable=True)
    sprint_time = Column(Time, nullable=True)


class Drivers(Base):
    __tablename__ = "drivers"

    driverId = Column(Integer, primary_key=True, autoincrement=True)
    driverRef = Column(String(255), nullable=False, default="")
    number = Column(Integer, default=None)
    code = Column(String(3), default=None)
    forename = Column(String(255), nullable=False, default="")
    surname = Column(String(255), nullable=False, default="")
    dob = Column(Date, default=None)
    nationality = Column(String(255), default=None)
    url = Column(String(255), nullable=False, default="")

    __table_args__ = (UniqueConstraint("url", name="url"),)


class LapData(Base):
    __tablename__ = "lapData"

    lapDataId = Column(Integer, primary_key=True, autoincrement=True)
    driverId = Column(Integer)
    raceId = Column(Integer)
    Time = Column(Time)
    RPM = Column(Integer)
    Speed = Column(Float)
    nGear = Column(Integer)
    Throttle = Column(Float)
    Brake = Column(Boolean)
    DRS = Column(Integer)
    Source = Column(String(255))
    RelativeDistance = Column(Float)
    Status = Column(String(255))
    X = Column(Float)
    Y = Column(Float)
    Z = Column(Float)
    Distance = Column(Float)
