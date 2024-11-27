# SAS-PRICES-PY: Python Package for Fetching SAS Flight Prices

## Overview

**SAS-PRICES-PY** is a Python package designed to interact with SAS (Scandinavian Airlines) flight pricing APIs. It provides functionality to fetch and process flight data, including round-trip prices for specified origins, destinations, regions, and durations. The package enables efficient data retrieval with support for asynchronous requests and custom filtering.

---

## Features

- **Cheapest Round Trips**:
  - Fetch the cheapest round-trip prices for specific destinations or entire regions.
  - Support for filtering by origin, destination, and trip start date.

- **Monthly Prices**:
  - Retrieve monthly outbound and inbound prices for specific origin-destination pairs.
  - Calculate combined round-trip prices for given months.

- **Trips by Length**:
  - Identify the cheapest trips of a specified duration (e.g., 2-day trips).
  - Option to search across all destinations or specific regions.

- **Batch Request Optimization**:
  - Simultaneous fetching of prices for multiple destinations using asynchronous requests for improved performance.

- **Error Handling**:
  - Gracefully handles API failures, empty responses, and invalid data.

---

## Installation

To install SAS-PRICES-PY, clone the repository and ensure the required dependencies are installed:

```bash
git clone https://github.com/alexechoi/sas-py.git
cd sas-py
pip install -r requirements.txt
```

---

## Usage

### 1. **Initialize the SAS Client**
```python
from sas.api import SAS

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

- **`sas/api.py`**:
  - Main interface for fetching data from the SAS API.
  - Provides methods for cheapest trips, monthly prices, and filtering by length.

- **`sas/sas_monthly.py`**:
  - Contains logic to fetch and process monthly round-trip prices.

- **`sas/sas_cheapest.py`**:
  - Implements fetching the cheapest round trips for multiple destinations.

- **`sas/data.py`**:
  - Defines available regions and their respective destinations.

- **`tests/test_api.py`**:
  - Unit tests to validate package functionality.

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

- `requests`
- `aiohttp`
- `brotli`
- `unittest`

Install them using:

```bash
pip install -r requirements.txt
```

---

## Development Notes

### Key Features
1. **Batch Requests**:
   - Optimized with asynchronous requests to reduce API call latency.

2. **Dynamic Filtering**:
   - Supports filtering by region, origin, destination, and trip duration.

3. **Customizable Markets**:
   - Set the market during initialization (`gb-en`, `us-en`, etc.).

### Known Limitations
- The API may return empty responses if no flights are available.
- Network-related errors can slow down or fail batch requests; retry mechanisms may be necessary.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

NOTE THAT THIS PROJECT IS IN NO WAY AFFILIATED WITH SCANDINAVIAN AIRLINES

---

## Contributions

Contributions are welcome! Please submit issues or pull requests via the [GitHub repository](https://github.com/alexechoi/sas-py).

--- 

## Author

Created by **Alex Choi**, November 2024.