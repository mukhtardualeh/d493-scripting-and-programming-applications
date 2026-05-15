"""
main.py
-------
D493 - Scripting and Programming Applications | WGU
Author : Mukhtar Dualeh

C3: Instantiates the WeatherData class (C1) and calls the three fetch
    methods (C2) to collect five-year historical weather data from the
    Open-Meteo API for Denver, CO on July 4.
"""

from weather_data import WeatherData

# Event location and date configuration
LOCATION_NAME = "Denver, Colorado"
LATITUDE = 39.7392        # decimal degrees N
LONGITUDE = -104.9903     # decimal degrees W
EVENT_MONTH = 7           # July
EVENT_DAY = 4             # 4th (Independence Day)


def main():
    """Entry point - fetch weather data for the chosen location and date."""
    print("=" * 60)
    print("  Weather Prediction Application - D493")
    print("  WGU Scripting and Programming - Applications")
    print("=" * 60)
    print(f"\nLocation : {LOCATION_NAME}")
    print(f"Date     : {EVENT_MONTH:02d}/{EVENT_DAY:02d} (five-year window: 2020-2024)\n")

    print("Fetching historical weather data from Open-Meteo API...")

    # C3: Create an instance of the WeatherData class
    weather = WeatherData(
        latitude=LATITUDE,
        longitude=LONGITUDE,
        month=EVENT_MONTH,
        day=EVENT_DAY,
    )

    # C3: Call each of the C2 fetch methods
    print("  - Fetching temperature data...")
    weather.fetch_temperature()

    print("  - Fetching wind speed data...")
    weather.fetch_wind_speed()

    print("  - Fetching precipitation data...")
    weather.fetch_precipitation()

    print("Data collection complete.\n")
    print(f"Avg Temp : {weather.avg_temperature} F")
    print(f"Max Wind : {weather.max_wind_speed} mph")
    print(f"Total Precip : {weather.sum_precipitation} in")


if __name__ == "__main__":
    main()
