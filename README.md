Here’s an updated version of your README tailored for a pip-distributed package:

---

# SAS-PRICES-PY: Python Package for Fetching SAS Flight Prices

## Overview

**SAS-PRICES-PY** is a Python package for interacting with SAS (Scandinavian Airlines) flight pricing APIs. It provides functionality to fetch and process flight data, including round-trip prices for specified origins, destinations, regions, and durations. Designed for efficiency, the package supports asynchronous requests and advanced filtering.

⚠️ **Disclaimer:** This package is in no way affiliated with Scandinavian Airlines.

---

## Features

- **Cheapest Round Trips**:
  - Fetch the cheapest round-trip prices for specific destinations or regions.
  - Filter results by origin, destination, and trip start date.

- **Monthly Prices**:
  - Retrieve monthly outbound and inbound prices for specific origin-destination pairs.
  - Calculate combined round-trip prices for selected months.

- **Trips by Length**:
  - Find the cheapest trips of a specified duration (e.g., 2-day trips).
  - Search across all destinations or specific regions.

- **Batch Request Optimization**:
  - Use asynchronous requests for faster data retrieval when fetching multiple destinations.

- **Error Handling**:
  - Handle API failures, empty responses, and invalid data gracefully.

---

## Installation

Install **SAS-PRICES-PY** via pip:

```bash
pip install sas-prices-py
```

---

## Usage

### 1. **Initialize the SAS Client**
```python
from sas_prices_py import SAS

sas = SAS(market="gb-en")  # Default market: "gb-en"
```

### 2. **Fetch Cheapest Round Trips**
```python
trips = sas.get_cheapest_round_trips(region="Europe", origin="LHR", start_date="2025-01-01")
print(trips)
```

### 3. **Fetch Monthly Round Trip Prices**
```python
monthly_trips = sas.get_monthly_round_trips(origin="LHR", destination="CPH", year_month="202501,202501")
print(monthly_trips)
```

### 4. **Fetch Cheapest Trips by Length**
```python
trips = sas.get_cheapest_trips_by_length(origin="LHR", destination="CPH", year_month="202501,202501", trip_length=2)
print(trips)
```

### 5. **Fetch Cheapest Trips Across All Destinations**
```python
trips = sas.get_cheapest_trips_by_length_all_destinations(
    origin="LHR", year_month="202501,202501", trip_length=2
)
print(trips)
```

---

## Code Structure

- **`sas_prices_py/api.py`**:
  - Main interface for interacting with SAS APIs.
  - Includes methods for fetching cheapest trips, monthly prices, and filtering by trip length.

- **`sas_prices_py/sas_monthly.py`**:
  - Handles monthly round-trip price logic.

- **`sas_prices_py/sas_cheapest.py`**:
  - Implements fetching the cheapest round trips.

- **`sas_prices_py/data.py`**:
  - Defines regions and their destinations.

- **`tests/test_api.py`**:
  - Unit tests for package functionality.

---

## Example Test Run

To run tests:

```bash
python -m unittest discover tests
```

Example output:

```
.....
----------------------------------------------------------------------
Ran 5 tests in 0.300s

OK
```

---

## Dependencies

The following dependencies are required and installed automatically with pip:

- `requests`
- `aiohttp`
- `brotli`

---

## Development Notes

### Key Features
1. **Batch Requests**:
   - Optimized with asynchronous requests to reduce API call latency.

2. **Dynamic Filtering**:
   - Filter by region, origin, destination, and trip duration.

3. **Customizable Markets**:
   - Set the market during initialization (`gb-en`, `us-en`, etc.).

### Known Limitations
- Empty responses may occur if no flights are available.
- Network-related errors can slow or fail batch requests; retry mechanisms may improve performance.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

**Disclaimer**: This project is in no way affiliated with Scandinavian Airlines.

---

## Contributions

Contributions are welcome! Please submit issues or pull requests via the [GitHub repository](https://github.com/alexechoi/sas-prices-py).

---

## Author

Created by **Alex Choi**, November 2024.