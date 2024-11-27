import requests
import brotli
import json
import logging
from typing import Dict, List

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_monthly_round_trip_prices(
    origin: str, destination: str, year_month: str, market: str = "gb-en"
) -> List[Dict]:
    """
    Fetch round trip prices for a given origin, destination, and month.

    Args:
        origin (str): Origin airport code.
        destination (str): Destination airport code.
        year_month (str): Year and month in the format YYYYMM (e.g., "202501").
        market (str): Market region (default is "gb-en").

    Returns:
        List[Dict]: List of dates with round trip prices.
    """
    BASE_URL = "https://www.sas.se/v2/cms-www-api/flights/calendar/prices/"
    HEADERS = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        ),
    }
    params = {
        "from": origin,
        "to": destination,
        "market": market,
        "month": year_month,
        "type": "adults-children",
        "flow": "revenue",
        "product": "All,All",
    }

    response = requests.get(BASE_URL, headers=HEADERS, params=params)

    # Handle encoding gracefully
    decoded_content = None
    try:
        content_encoding = response.headers.get("Content-Encoding", "").lower()
        if content_encoding == "br":
            decoded_content = response.content.decode("utf-8")
        elif content_encoding in ["gzip", "deflate"]:
            decoded_content = response.content.decode("utf-8")
        else:
            decoded_content = response.text
    except Exception as e:
        logger.error(f"Decompression or decoding failed: {e}")
        return []

    # Parse JSON and calculate combined round trip prices
    try:
        data = json.loads(decoded_content)
        outbound = data.get("outbound", {})
        inbound = data.get("inbound", {})

        # Warn if inbound is empty
        if not inbound:
            logger.warning("Inbound data is missing or empty; only outbound prices will be considered.")

        round_trip_prices = []

        # Calculate round-trip prices or fallback to outbound-only prices
        for out_date, out_price in outbound.items():
            if inbound:
                for in_date, in_price in inbound.items():
                    try:
                        round_trip_prices.append({
                            "outbound_date": out_date,
                            "inbound_date": in_date,
                            "round_trip_price": out_price["totalPrice"] + in_price["totalPrice"]
                        })
                    except KeyError:
                        logger.warning(f"Missing price data for dates: {out_date}, {in_date}")
            else:
                # If no inbound data, return outbound prices only
                try:
                    round_trip_prices.append({
                        "outbound_date": out_date,
                        "inbound_date": None,
                        "round_trip_price": out_price["totalPrice"]
                    })
                except KeyError:
                    logger.warning(f"Missing outbound price data for date: {out_date}")

        return sorted(round_trip_prices, key=lambda x: x["round_trip_price"])
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}")
        return []