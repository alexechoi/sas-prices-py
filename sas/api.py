import requests
import brotli
import json
from typing import List, Dict
import logging
from sas.data import regions

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SAS:
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

    def __init__(self, market: str = "gb-en", origin: str = "LHR"):
        self.market = market
        self.origin = origin

    def get_cheapest_round_trips(
        self,
        destinations: str = None,
        start_date: str = None,
        region: str = None,
        origin: str = None,
    ) -> List[Dict]:
        """
        Fetch the cheapest round trips for the specified destinations or region.

        Args:
            destinations (str): Comma-separated list of destination airport codes.
            start_date (str): The campaign start date (e.g., "2024-11-25").
            region (str): Optional region name (e.g., "Europe").
            origin (str): Optional origin airport code (overrides default).

        Returns:
            List[Dict]: A list of the cheapest trips or an empty list if no trips are found.
        """
        if region:
            if region not in regions:
                logger.error(f"Invalid region: {region}. Available regions: {', '.join(regions.keys())}")
                return []
            destinations = regions[region]

        if not destinations:
            logger.error("No destinations provided or resolved from the region.")
            return []

        params = {
            "market": self.market,
            "origin": origin or self.origin,
            "destinations": destinations,
            "type": "R",  # Round trip
            "sorting": "cities",
            "campaignStartDate": start_date,
        }

        response = requests.get(self.BASE_URL, headers=self.HEADERS, params=params)

        # Log the API response
        logger.info(f"API Response: {response.status_code} - {response.text[:500]}")

        # Handle Brotli-encoded content
        decoded_content = None
        if response.headers.get("Content-Encoding") == "br":
            try:
                decoded_content = brotli.decompress(response.content).decode("utf-8")
            except Exception as e:
                logger.error(f"Brotli decompression failed: {e}")
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