"""
test_weather.py
---------------
D493 - Scripting and Programming Applications | WGU
Author : Mukhtar Dualeh

E: Unit tests for the WeatherData class (weather_data.py).

   Tests cover:
     - Correct initialization of all instance variables (C1).
     - The fetch_temperature method returns valid numeric aggregates (C2).
     - The fetch_wind_speed method returns valid numeric aggregates (C2).
     - The fetch_precipitation method returns valid numeric aggregates (C2).

   Run with:
       python -m pytest test_weather.py -v
   or:
       python test_weather.py
"""

import unittest
from unittest.mock import MagicMock, patch

from weather_data import WeatherData


class TestWeatherDataInit(unittest.TestCase):
    """Tests for WeatherData.__init__ (C1 instance variables)."""

    def setUp(self):
        """Create a WeatherData instance for Denver, CO on July 4."""
        self.weather = WeatherData(
            latitude=39.7392,
            longitude=-104.9903,
            month=7,
            day=4,
        )

    def test_latitude_stored_correctly(self):
        """Instance variable latitude should equal the value passed in."""
        self.assertEqual(self.weather.latitude, 39.7392)

    def test_longitude_stored_correctly(self):
        """Instance variable longitude should equal the value passed in."""
        self.assertEqual(self.weather.longitude, -104.9903)

    def test_month_stored_correctly(self):
        """Instance variable month should equal the value passed in."""
        self.assertEqual(self.weather.month, 7)

    def test_day_stored_correctly(self):
        """Instance variable day should equal the value passed in."""
        self.assertEqual(self.weather.day, 4)

    def test_year_set_to_most_recent(self):
        """Instance variable year should default to the most recent year (2024)."""
        self.assertEqual(self.weather.year, 2024)

    def test_temperature_vars_initialized_to_none(self):
        """Temperature instance variables should be None before fetching."""
        self.assertIsNone(self.weather.avg_temperature)
        self.assertIsNone(self.weather.min_temperature)
        self.assertIsNone(self.weather.max_temperature)

    def test_wind_vars_initialized_to_none(self):
        """Wind speed instance variables should be None before fetching."""
        self.assertIsNone(self.weather.avg_wind_speed)
        self.assertIsNone(self.weather.min_wind_speed)
        self.assertIsNone(self.weather.max_wind_speed)

    def test_precipitation_vars_initialized_to_none(self):
        """Precipitation instance variables should be None before fetching."""
        self.assertIsNone(self.weather.sum_precipitation)
        self.assertIsNone(self.weather.min_precipitation)
        self.assertIsNone(self.weather.max_precipitation)


class TestFetchTemperature(unittest.TestCase):
    """Tests for WeatherData.fetch_temperature (C2)."""

    def _make_api_response(self, mean, high, low):
        """Build a mock daily dict matching Open-Meteo response shape."""
        return {
            "temperature_2m_mean": [mean],
            "temperature_2m_max": [high],
            "temperature_2m_min": [low],
        }

    def test_fetch_temperature_sets_instance_variables(self):
        """fetch_temperature should populate avg, min, and max temperature."""
        weather = WeatherData(39.7392, -104.9903, 7, 4)

        # Patch _fetch_single_day to return controlled data for all 5 years
        side_effects = [
            self._make_api_response(74.8, 89.0, 64.4),
            self._make_api_response(72.1, 84.6, 60.3),
            self._make_api_response(77.9, 92.5, 63.0),
            self._make_api_response(68.2, 80.2, 56.2),
            self._make_api_response(70.5, 82.9, 56.2),
        ]

        with patch.object(weather, "_fetch_single_day", side_effect=side_effects):
            result = weather.fetch_temperature()

        # Five-year average mean: (74.8+72.1+77.9+68.2+70.5) / 5 = 72.7
        self.assertAlmostEqual(result["avg_temperature"], 72.7, places=1)
        # Five-year minimum: min of [64.4, 60.3, 63.0, 56.2, 56.2]
        self.assertAlmostEqual(result["min_temperature"], 56.2, places=1)
        # Five-year maximum: max of [89.0, 84.6, 92.5, 80.2, 82.9]
        self.assertAlmostEqual(result["max_temperature"], 92.5, places=1)

        # Confirm instance variables were also set
        self.assertEqual(weather.avg_temperature, result["avg_temperature"])
        self.assertEqual(weather.min_temperature, result["min_temperature"])
        self.assertEqual(weather.max_temperature, result["max_temperature"])

    def test_fetch_temperature_returns_dict_with_correct_keys(self):
        """fetch_temperature should return a dict with the three expected keys."""
        weather = WeatherData(39.7392, -104.9903, 7, 4)
        daily_stub = self._make_api_response(70.0, 85.0, 55.0)

        with patch.object(weather, "_fetch_single_day", return_value=daily_stub):
            result = weather.fetch_temperature()

        self.assertIn("avg_temperature", result)
        self.assertIn("min_temperature", result)
        self.assertIn("max_temperature", result)


class TestFetchWindSpeed(unittest.TestCase):
    """Tests for WeatherData.fetch_wind_speed (C2)."""

    def _make_wind_response(self, speed):
        return {"wind_speed_10m_max": [speed]}

    def test_fetch_wind_speed_computes_correct_aggregates(self):
        """fetch_wind_speed should compute avg, min, and max over five years."""
        weather = WeatherData(39.7392, -104.9903, 7, 4)
        speeds = [11.7, 11.0, 15.5, 15.9, 15.9]
        side_effects = [self._make_wind_response(s) for s in speeds]

        with patch.object(weather, "_fetch_single_day", side_effect=side_effects):
            result = weather.fetch_wind_speed()

        expected_avg = round(sum(speeds) / len(speeds), 2)
        self.assertAlmostEqual(result["avg_wind_speed"], expected_avg, places=2)
        self.assertAlmostEqual(result["min_wind_speed"], min(speeds), places=2)
        self.assertAlmostEqual(result["max_wind_speed"], max(speeds), places=2)

    def test_fetch_wind_speed_sets_instance_variables(self):
        """fetch_wind_speed should update the instance variables."""
        weather = WeatherData(39.7392, -104.9903, 7, 4)
        with patch.object(weather, "_fetch_single_day",
                          return_value={"wind_speed_10m_max": [12.5]}):
            weather.fetch_wind_speed()

        self.assertIsNotNone(weather.avg_wind_speed)
        self.assertIsNotNone(weather.min_wind_speed)
        self.assertIsNotNone(weather.max_wind_speed)


class TestFetchPrecipitation(unittest.TestCase):
    """Tests for WeatherData.fetch_precipitation (C2)."""

    def _make_precip_response(self, amount):
        return {"precipitation_sum": [amount]}

    def test_fetch_precipitation_computes_correct_sum(self):
        """fetch_precipitation should compute the five-year total sum."""
        weather = WeatherData(39.7392, -104.9903, 7, 4)
        amounts = [0.02, 0.063, 0.0, 0.256, 0.0]
        side_effects = [self._make_precip_response(a) for a in amounts]

        with patch.object(weather, "_fetch_single_day", side_effect=side_effects):
            result = weather.fetch_precipitation()

        expected_sum = round(sum(amounts), 4)
        self.assertAlmostEqual(result["sum_precipitation"], expected_sum, places=4)
        self.assertAlmostEqual(result["min_precipitation"], min(amounts), places=4)
        self.assertAlmostEqual(result["max_precipitation"], max(amounts), places=4)

    def test_fetch_precipitation_returns_correct_keys(self):
        """fetch_precipitation should return a dict with three expected keys."""
        weather = WeatherData(39.7392, -104.9903, 7, 4)
        with patch.object(weather, "_fetch_single_day",
                          return_value={"precipitation_sum": [0.1]}):
            result = weather.fetch_precipitation()

        self.assertIn("sum_precipitation", result)
        self.assertIn("min_precipitation", result)
        self.assertIn("max_precipitation", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
