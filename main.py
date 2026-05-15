"""
main.py
-------
D493 - Scripting and Programming Applications | WGU
Author : Mukhtar Dualeh

C3: Instantiates the WeatherData class (C1) and calls the three fetch
    methods (C2) to collect five-year historical weather data from the
    Open-Meteo API for Denver, CO on July 4.

C5: Populates the SQLite 'weather_records' table (created in C4) with
    the collected weather data using the SQLAlchemy ORM.
"""

from weather_data import WeatherData
from database import WeatherRecord, get_engine, init_db, get_session

# Event location and date configuration
LOCATION_NAME = "Denver, Colorado"
LATITUDE = 39.7392        # decimal degrees N
LONGITUDE = -104.9903     # decimal degrees W
EVENT_MONTH = 7           # July
EVENT_DAY = 4             # 4th (Independence Day)


def main():
    """Entry point - fetch, store, and display weather data."""
    print("=" * 60)
    print("  Weather Prediction Application - D493")
    print("  WGU Scripting and Programming - Applications")
    print("=" * 60)
    print(f"\nLocation : {LOCATION_NAME}")
    print(f"Date     : {EVENT_MONTH:02d}/{EVENT_DAY:02d} (five-year window: 2020-2024)\n")

    # C3: Instantiate WeatherData and call the three C2 fetch methods
    print("Fetching historical weather data from Open-Meteo API...")
    weather = WeatherData(
        latitude=LATITUDE,
        longitude=LONGITUDE,
        month=EVENT_MONTH,
        day=EVENT_DAY,
    )
    print("  - Fetching temperature data...")
    weather.fetch_temperature()
    print("  - Fetching wind speed data...")
    weather.fetch_wind_speed()
    print("  - Fetching precipitation data...")
    weather.fetch_precipitation()
    print("Data collection complete.\n")

    # C5: Populate the SQLite table with the collected weather data
    print("Saving data to SQLite database (weather_data.db)...")
    engine = get_engine()
    init_db(engine)           # create the table if it does not exist

    session = get_session(engine)

    # Build a WeatherRecord ORM object from the WeatherData instance
    record = WeatherRecord(
        location_name=LOCATION_NAME,
        latitude=weather.latitude,
        longitude=weather.longitude,
        month=weather.month,
        day=weather.day,
        year=weather.year,
        avg_temperature=weather.avg_temperature,
        min_temperature=weather.min_temperature,
        max_temperature=weather.max_temperature,
        avg_wind_speed=weather.avg_wind_speed,
        min_wind_speed=weather.min_wind_speed,
        max_wind_speed=weather.max_wind_speed,
        sum_precipitation=weather.sum_precipitation,
        min_precipitation=weather.min_precipitation,
        max_precipitation=weather.max_precipitation,
    )
    session.add(record)
    session.commit()
    print(f"Record saved with ID: {record.id}\n")
    session.close()


if __name__ == "__main__":
    main()
