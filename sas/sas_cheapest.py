import requests
import brotli
import json
import logging
from typing import List, Dict

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_cheapest_round_trips(
    market: str,
    origin: str,
    destinations: str,
    start_date: str
) -> List[Dict]:
    """
    Fetch the cheapest round trips for multiple destinations.

    Args:
        market (str): Market region (e.g., "gb-en").
        origin (str): Origin airport code.
        destinations (str): Comma-separated list of destination airport codes.
        start_date (str): Campaign start date (e.g., "2024-11-25").

    Returns:
        List[Dict]: A list of the cheapest trips or an empty list if no trips are found.
    """
    BASE_URL = "https://www.flysas.com/v2/cms-price-api/prices/"
    HEADERS = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "www.flysas.com",
        "Referer": "https://www.flysas.com/",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        ),
    }

    params = {
        "market": market,
        "origin": origin,
        "destinations": destinations,
        "type": "R",  # Round trip
        "sorting": "cities",
        "campaignStartDate": start_date,
    }

    response = requests.get(BASE_URL, headers=HEADERS, params=params)

    # Log the API response
    logger.info(f"API Response: {response.status_code} - {response.text[:500]}")

    # Handle Brotli-encoded content
    decoded_content = None
    if response.headers.get("Content-Encoding") == "br":
        try:
            decoded_content = brotli.decompress(response.content).decode("utf-8")
        except Exception as e:
            decoded_content = response.text  # Fallback to raw content
    else:
        decoded_content = response.text

    # Parse JSON
    try:
        data = json.loads(decoded_content)
        if not isinstance(data, list) or not all("prices" in dest for dest in data):
            logger.error("Unexpected data structure in API response")
            return []
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}")
        return []