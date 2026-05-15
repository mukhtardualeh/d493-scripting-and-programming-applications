"""
weather_data.py
---------------
D493 - Scripting and Programming Applications | WGU
Author : Mukhtar Dualeh

C1: Defines the WeatherData class with instance variables for a chosen
    US location (Denver, CO) and date (July 4), plus five-year aggregate
    statistics for temperature, wind speed, and precipitation.
"""


class WeatherData:
    """
    Represents five-year historical weather statistics for a specific
    location and calendar date.

    Instance Variables
    ------------------
    latitude          : float - Location latitude in decimal degrees.
    longitude         : float - Location longitude in decimal degrees.
    month             : int   - Month of the event (1-12).
    day               : int   - Day of the month for the event (1-31).
    year              : int   - Most recent year in the five-year window.

    avg_temperature   : float - Five-year average mean temperature (F).
    min_temperature   : float - Five-year minimum temperature (F).
    max_temperature   : float - Five-year maximum temperature (F).

    avg_wind_speed    : float - Five-year average max wind speed (mph).
    min_wind_speed    : float - Five-year minimum max wind speed (mph).
    max_wind_speed    : float - Five-year maximum max wind speed (mph).

    sum_precipitation : float - Five-year total precipitation sum (in).
    min_precipitation : float - Five-year minimum daily precipitation (in).
    max_precipitation : float - Five-year maximum daily precipitation (in).
    """

    # Open-Meteo historical archive endpoint
    _API_URL = "https://archive-api.open-meteo.com/v1/archive"

    # Years to include in the five-year window
    _YEARS = [2020, 2021, 2022, 2023, 2024]

    def __init__(self, latitude: float, longitude: float, month: int, day: int):
        """
        Initialize WeatherData with location coordinates and a calendar date.

        Parameters
        ----------
        latitude  : float - Location latitude in decimal degrees.
        longitude : float - Location longitude in decimal degrees.
        month     : int   - Month of the event (1-12).
        day       : int   - Day of the month for the event (1-31).
        """
        # --- Location and date instance variables ---
        self.latitude = latitude
        self.longitude = longitude
        self.month = month
        self.day = day
        self.year = max(self._YEARS)  # most recent year in the window

        # --- Temperature instance variables (Fahrenheit) ---
        self.avg_temperature = None   # five-year average mean temperature
        self.min_temperature = None   # five-year minimum temperature
        self.max_temperature = None   # five-year maximum temperature

        # --- Wind speed instance variables (mph) ---
        self.avg_wind_speed = None    # five-year average max wind speed
        self.min_wind_speed = None    # five-year minimum max wind speed
        self.max_wind_speed = None    # five-year maximum max wind speed

        # --- Precipitation instance variables (inches) ---
        self.sum_precipitation = None  # five-year total precipitation sum
        self.min_precipitation = None  # five-year minimum daily precipitation
        self.max_precipitation = None  # five-year maximum daily precipitation
