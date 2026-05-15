"""
database.py
-----------
D493 - Scripting and Programming Applications | WGU
Author : Mukhtar Dualeh

C4: Defines the WeatherRecord SQLAlchemy ORM model, which maps to a SQLite
    table called 'weather_records'. The table includes a field for every
    instance variable defined in the WeatherData class (C1).

    Also exposes helper functions to create the table and open a database
    session so that main.py can populate (C5) and query (C6) records.
"""

import os

from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Base class for all ORM models
Base = declarative_base()

# SQLite database file stored in the same directory as this module
_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = "sqlite:///" + os.path.join(_DIR, "weather_data.db")


class WeatherRecord(Base):
    """
    SQLAlchemy ORM model representing one row in the 'weather_records' table.

    Each row stores the five-year historical weather aggregates for a
    specific location (latitude/longitude) and calendar date (month/day/year).

    Columns mirror all instance variables from the WeatherData class (C1):
      - Location  : latitude, longitude
      - Date      : month, day, year
      - Label     : location_name (human-readable)
      - Temp (F)  : avg_temperature, min_temperature, max_temperature
      - Wind (mph): avg_wind_speed,  min_wind_speed,  max_wind_speed
      - Precip(in): sum_precipitation, min_precipitation, max_precipitation
    """

    __tablename__ = "weather_records"

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Location fields
    location_name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Date fields
    month = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

    # Five-year temperature fields (Fahrenheit)
    avg_temperature = Column(Float)
    min_temperature = Column(Float)
    max_temperature = Column(Float)

    # Five-year wind speed fields (mph)
    avg_wind_speed = Column(Float)
    min_wind_speed = Column(Float)
    max_wind_speed = Column(Float)

    # Five-year precipitation fields (inches)
    sum_precipitation = Column(Float)
    min_precipitation = Column(Float)
    max_precipitation = Column(Float)

    def __repr__(self):
        return (
            "<WeatherRecord(id={}, location='{}', date={:02d}/{:02d}/{})>".format(
                self.id, self.location_name, self.month, self.day, self.year
            )
        )


def get_engine(db_url=None):
    """
    Create and return a SQLAlchemy engine connected to the SQLite database.

    Parameters
    ----------
    db_url : str or None
        Connection string. Defaults to the local SQLite file (DATABASE_URL).

    Returns
    -------
    sqlalchemy.engine.Engine
    """
    if db_url is None:
        db_url = DATABASE_URL
    engine = create_engine(db_url, echo=False)
    return engine


def init_db(engine=None):
    """
    Create all tables defined in Base.metadata if they do not already exist.

    Parameters
    ----------
    engine : Engine or None
        Uses the default DATABASE_URL engine when None.
    """
    if engine is None:
        engine = get_engine()
    Base.metadata.create_all(engine)


def get_session(engine=None):
    """
    Return a new SQLAlchemy Session bound to the given engine.

    Parameters
    ----------
    engine : Engine or None
        Uses the default DATABASE_URL engine when None.

    Returns
    -------
    sqlalchemy.orm.Session
    """
    if engine is None:
        engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()
