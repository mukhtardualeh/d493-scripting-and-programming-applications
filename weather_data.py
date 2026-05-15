"""
weather_data.py
---------------
D493 - Scripting and Programming Applications | WGU
Author : Mukhtar Dualeh

C1: Defines the WeatherData class with instance variables for a chosen
    US location (Denver, CO) and date (July 4), plus five-year aggregate
    statistics for temperature, wind speed, and precipitation.

C2: Provides three methods that call the Open-Meteo Historical Weather API
    to fetch data for the most recent five years (2020-2024) and compute
    the aggregate values stored in the instance variables.
"""

import requests


class WeatherData:
    """
    Represents five-year historical weather statistics for a specific
    location and calendar date.

    The class fetches data from the Open-Meteo Historical Weather API
    (https://open-meteo.com/en/docs/historical-weather-api) for the
    chosen month/day across years 2020-2024 and stores the computed
    aggregate values as instance variables.

    Instance Variables
    ------------------
    latitude  : float  - Location latitude in decimal degrees.
    longitude : float  - Location longitude in decimal degrees.
    month     : int    - Month of the event (1-12).
    day       : int    - Day of the month for the event (1-31).
    year      : int    - Most recent year in the five-year window.

    avg_temperature : float - Five-year average mean temperature (°F).
    min_temperature : float - Five-year minimum temperature (°F).
    max_temperature : float - Five-year maximum temperature (°F).

    avg_wind_speed  : float - Five-year average max wind speed (mph).
    min_wind_speed  : float - Five-year minimum max wind speed (mph).
    max_wind_speed  : float - Five-year maximum max wind speed (mph).

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

    # ------------------------------------------------------------------
    # Private helper
    # ------------------------------------------------------------------

    def _fetch_single_day(self, year: int, variables: str) -> dict:
        """
        Call the Open-Meteo archive API for a single date and return the
        'daily' portion of the JSON response.

        Parameters
        ----------
        year      : int - The year to query (e.g. 2022).
        variables : str - Comma-separated daily variable names.

        Returns
        -------
        dict - The 'daily' key from the API JSON response.
        """
        date_str = f"{year}-{self.month:02d}-{self.day:02d}"
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "start_date": date_str,
            "end_date": date_str,
            "daily": variables,
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
            "precipitation_unit": "inch",
            "timezone": "America/Denver",
        }
        response = requests.get(self._API_URL, params=params, timeout=15)
        response.raise_for_status()
        return response.json().get("daily", {})

    # ------------------------------------------------------------------
    # C2 Methods: one per required weather variable category
    # ------------------------------------------------------------------

    def fetch_temperature(self) -> dict:
        """
        C2 - Fetch mean temperature (°F) for the chosen location and date
        over the most recent five years using the Open-Meteo Historical
        Weather API.

        Populates
        ---------
        self.avg_temperature, self.min_temperature, self.max_temperature

        Returns
        -------
        dict - Keys: avg_temperature, min_temperature, max_temperature.
        """
        means, mins, maxs = [], [], []

        for year in self._YEARS:
            # Request mean, max, and min daily temperature
            daily = self._fetch_single_day(
                year,
                "temperature_2m_mean,temperature_2m_max,temperature_2m_min"
            )
            mean_val = daily.get("temperature_2m_mean", [None])[0]
            max_val = daily.get("temperature_2m_max", [None])[0]
            min_val = daily.get("temperature_2m_min", [None])[0]

            if mean_val is not None:
                means.append(mean_val)
            if max_val is not None:
                maxs.append(max_val)
            if min_val is not None:
                mins.append(min_val)

        # Compute five-year aggregates
        self.avg_temperature = round(sum(means) / len(means), 2) if means else None
        self.min_temperature = round(min(mins), 2) if mins else None
        self.max_temperature = round(max(maxs), 2) if maxs else None

        return {
            "avg_temperature": self.avg_temperature,
            "min_temperature": self.min_temperature,
            "max_temperature": self.max_temperature,
        }

    def fetch_wind_speed(self) -> dict:
        """
        C2 - Fetch maximum wind speed (mph) for the chosen location and date
        over the most recent five years using the Open-Meteo Historical
        Weather API.

        Populates
        ---------
        self.avg_wind_speed, self.min_wind_speed, self.max_wind_speed

        Returns
        -------
        dict - Keys: avg_wind_speed, min_wind_speed, max_wind_speed.
        """
        wind_speeds = []

        for year in self._YEARS:
            # Request daily maximum wind speed at 10 m
            daily = self._fetch_single_day(year, "wind_speed_10m_max")
            wind_val = daily.get("wind_speed_10m_max", [None])[0]
            if wind_val is not None:
                wind_speeds.append(wind_val)

        # Compute five-year aggregates
        self.avg_wind_speed = round(sum(wind_speeds) / len(wind_speeds), 2) if wind_speeds else None
        self.min_wind_speed = round(min(wind_speeds), 2) if wind_speeds else None
        self.max_wind_speed = round(max(wind_speeds), 2) if wind_speeds else None

        return {
            "avg_wind_speed": self.avg_wind_speed,
            "min_wind_speed": self.min_wind_speed,
            "max_wind_speed": self.max_wind_speed,
        }

    def fetch_precipitation(self) -> dict:
        """
        C2 - Fetch precipitation sum (inches) for the chosen location and date
        over the most recent five years using the Open-Meteo Historical
        Weather API.

        Populates
        ---------
        self.sum_precipitation, self.min_precipitation, self.max_precipitation

        Returns
        -------
        dict - Keys: sum_precipitation, min_precipitation, max_precipitation.
        """
        daily_precips = []

        for year in self._YEARS:
            # Request daily precipitation sum
            daily = self._fetch_single_day(year, "precipitation_sum")
            precip_val = daily.get("precipitation_sum", [None])[0]
            if precip_val is not None:
                daily_precips.append(precip_val)

        # Compute five-year aggregates
        self.sum_precipitation = round(sum(daily_precips), 4) if daily_precips else None
        self.min_precipitation = round(min(daily_precips), 4) if daily_precips else None
        self.max_precipitation = round(max(daily_precips), 4) if daily_precips else None

        return {
            "sum_precipitation": self.sum_precipitation,
            "min_precipitation": self.min_precipitation,
            "max_precipitation": self.max_precipitation,
        }
