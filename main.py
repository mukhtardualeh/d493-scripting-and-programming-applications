"""
main.py
-------
D493 - Scripting and Programming Applications | WGU
Author : Mukhtar Dualeh

C3: Instantiates the WeatherData class (C1) and calls the three fetch methods
    (C2) to collect five-year historical weather data from the Open-Meteo API
    for Denver, CO on July 4.

C5: Populates the SQLite 'weather_records' table (created in C4) with the
    collected weather data using the SQLAlchemy ORM.

C6: Queries the record just inserted, then prints a formatted summary of the
    stored data to the console.
"""

from weather_data import WeatherData
from database import WeatherRecord, get_engine, init_db, get_session


# -----------------------------------------------------------------------
# Event location and date configuration
# -----------------------------------------------------------------------

LOCATION_NAME = "Denver, Colorado"
LATITUDE = 39.7392        # decimal degrees N
LONGITUDE = -104.9903     # decimal degrees W
EVENT_MONTH = 7           # July
EVENT_DAY = 4             # 4th (Independence Day)


def main():
    """
    Entry point for the Weather Prediction application.

    Steps performed:
      1. (C3) Create a WeatherData instance and call the three fetch methods.
      2. (C5) Open the SQLite database, create the table if needed, and insert
              the collected weather data as a new WeatherRecord row.
      3. (C6) Query the inserted record and print a formatted report.
    """

    # ---------------------------------------------------------------
    # C3: Create WeatherData instance and call C2 fetch methods
    # ---------------------------------------------------------------
    print("=" * 60)
    print("  Weather Prediction Application - D493")
    print("  WGU Scripting and Programming - Applications")
    print("=" * 60)
    print(f"\nLocation : {LOCATION_NAME}")
    print(f"Date     : {EVENT_MONTH:02d}/{EVENT_DAY:02d} (five-year window: 2020-2024)\n")

    print("Fetching historical weather data from Open-Meteo API...")

    # Instantiate the WeatherData class (C1 instance variables initialized here)
    weather = WeatherData(
        latitude=LATITUDE,
        longitude=LONGITUDE,
        month=EVENT_MONTH,
        day=EVENT_DAY,
    )

    # C2 Method 1: fetch mean temperature in Fahrenheit
    print("  - Fetching temperature data...")
    weather.fetch_temperature()

    # C2 Method 2: fetch maximum wind speed in mph
    print("  - Fetching wind speed data...")
    weather.fetch_wind_speed()

    # C2 Method 3: fetch precipitation sum in inches
    print("  - Fetching precipitation data...")
    weather.fetch_precipitation()

    print("Data collection complete.\n")

    # ---------------------------------------------------------------
    # C5: Populate the SQLite table with the collected weather data
    # ---------------------------------------------------------------
    print("Saving data to SQLite database (weather_data.db)...")

    engine = get_engine()
    init_db(engine)           # create table if it does not exist
    session = get_session(engine)

    # Build a new WeatherRecord ORM object from the WeatherData instance
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
    inserted_id = record.id
    print(f"Record saved with ID: {inserted_id}\n")

    # ---------------------------------------------------------------
    # C6: Query the table and display the formatted data on screen
    # ---------------------------------------------------------------
    print("Querying the database for the stored record...\n")

    queried = session.query(WeatherRecord).filter_by(id=inserted_id).one()

    # Format and print a readable report
    print("=" * 60)
    print("  FIVE-YEAR HISTORICAL WEATHER REPORT")
    print("=" * 60)
    print(f"  Record ID       : {queried.id}")
    print(f"  Location        : {queried.location_name}")
    print(f"  Latitude        : {queried.latitude}° N")
    print(f"  Longitude       : {queried.longitude}° W")
    print(f"  Event Date      : {queried.month:02d}/{queried.day:02d}")
    print(f"  Data Year Range : 2020 - {queried.year}")
    print("-" * 60)
    print("  TEMPERATURE (°F)")
    print(f"    5-Year Average : {queried.avg_temperature:.2f} °F")
    print(f"    5-Year Minimum : {queried.min_temperature:.2f} °F")
    print(f"    5-Year Maximum : {queried.max_temperature:.2f} °F")
    print("-" * 60)
    print("  WIND SPEED (mph)")
    print(f"    5-Year Average : {queried.avg_wind_speed:.2f} mph")
    print(f"    5-Year Minimum : {queried.min_wind_speed:.2f} mph")
    print(f"    5-Year Maximum : {queried.max_wind_speed:.2f} mph")
    print("-" * 60)
    print("  PRECIPITATION (inches)")
    print(f"    5-Year Total   : {queried.sum_precipitation:.4f} in")
    print(f"    5-Year Minimum : {queried.min_precipitation:.4f} in")
    print(f"    5-Year Maximum : {queried.max_precipitation:.4f} in")
    print("=" * 60)

    session.close()


if __name__ == "__main__":
    main()
