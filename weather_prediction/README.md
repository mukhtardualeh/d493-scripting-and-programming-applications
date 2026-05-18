# Weather Prediction Application
**D493 - Scripting and Programming Applications | WGU**
**Author: Mukhtar Dualeh**

---

## Overview

This application collects five years of historical weather data for a specific United States location and calendar date using the Open-Meteo Historical Weather API (Zippenfenig, 2023). The collected data is stored in a local SQLite database through the SQLAlchemy ORM and then queried and displayed in a formatted console report.

- **Location:** Denver, Colorado (39.7392° N, 104.9903° W)
- **Date:** July 4 (Independence Day)
- **Data Window:** 2020 through 2024 (five years)

The Open-Meteo API provides free access to historical weather data without requiring an API key (Zippenfenig, 2023). All temperature values are reported in Fahrenheit, wind speed in miles per hour, and precipitation in inches.

---

## Project Structure

```
weather_prediction/
├── weather_data.py    # WeatherData class: instance variables (C1) and API methods (C2)
├── database.py        # SQLAlchemy ORM model and database helper functions (C4)
├── main.py            # Entry point: fetch, store, and display weather data (C3, C5, C6)
├── test_weather.py    # Unit tests for WeatherData methods (D)
├── requirements.txt   # Python package dependencies (E)
├── screenshots/       # Program output and test execution screenshots
└── README.md          # Project documentation (B)
```

---

## Prerequisites

- Python 3.10 or later
- pip (Python package manager)

---

## Installation

1. Clone the repository:

```bash
git clone https://gitlab.com/wgu-gitlab-environment/student-repos/mdualeh1/d493-scripting-and-programming-applications.git
cd d493-scripting-and-programming-applications/weather_prediction
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Running the Program

From inside the `weather_prediction/` directory, run:

```bash
python main.py
```

**Expected Output:**

```
============================================================
  Weather Prediction Application - D493
  WGU Scripting and Programming - Applications
============================================================

Location : Denver, Colorado
Date     : 07/04 (five-year window: 2020-2024)

Fetching historical weather data from Open-Meteo API...
  - Fetching temperature data...
  - Fetching wind speed data...
  - Fetching precipitation data...
Data collection complete.

Saving data to SQLite database (weather_data.db)...
Record saved with ID: 1

Querying the database for the stored record...

============================================================
  FIVE-YEAR HISTORICAL WEATHER REPORT
============================================================
  Record ID       : 1
  Location        : Denver, Colorado
  Latitude        : 39.7392° N
  Longitude       : -104.9903° W
  Event Date      : 07/04
  Data Year Range : 2020 - 2024
------------------------------------------------------------
  TEMPERATURE (°F)
    5-Year Average : 72.70 °F
    5-Year Minimum : 56.20 °F
    5-Year Maximum : 92.50 °F
------------------------------------------------------------
  WIND SPEED (mph)
    5-Year Average : 14.00 mph
    5-Year Minimum : 11.00 mph
    5-Year Maximum : 15.90 mph
------------------------------------------------------------
  PRECIPITATION (inches)
    5-Year Total   : 0.3390 in
    5-Year Minimum : 0.0000 in
    5-Year Maximum : 0.2560 in
============================================================
```

A SQLite database file named `weather_data.db` is created in the project directory on the first run. Each subsequent run adds an additional row to the table.

---

## Running the Unit Tests

```bash
python -m pytest test_weather.py -v
```

or without pytest:

```bash
python test_weather.py
```

---

## Screenshots

The `screenshots/` folder contains the following program execution evidence:

- **ide_clone.png** — Project cloned and opened in the IDE
- **program_output.png** — Console output from running `main.py`, including the database query results (C6)
- **test_results.png** — All unit tests passing when running `python -m pytest test_weather.py -v`

---

## Data Source

All weather data is retrieved from the Open-Meteo Historical Weather API, which provides free access to historical meteorological records with no API key required (Zippenfenig, 2023):

```
https://archive-api.open-meteo.com/v1/archive
```

| Parameter | Value |
|---|---|
| latitude | 39.7392 |
| longitude | -104.9903 |
| start_date / end_date | YYYY-07-04 (one year at a time) |
| daily variables | temperature_2m_mean, temperature_2m_max, temperature_2m_min, wind_speed_10m_max, precipitation_sum |
| temperature_unit | fahrenheit |
| wind_speed_unit | mph |
| precipitation_unit | inch |
| timezone | America/Denver |

---

## References

Zippenfenig, P. (2023). *Open-Meteo.com Weather API* [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.7970649
