import aiohttp
import asyncio
import logging
import json
from typing import List, Dict
import brotli

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


async def fetch_prices(
    session: aiohttp.ClientSession, origin: str, destination: str, year_month: str, market: str
) -> Dict:
    """
    Fetch monthly round trip prices for a single origin-destination pair.
    """
    params = {
        "from": origin,
        "to": destination,
        "market": market,
        "month": year_month,
        "type": "adults-children",
        "flow": "revenue",
        "product": "All,All",
    }

    try:
        async with session.get(BASE_URL, headers=HEADERS, params=params) as response:
            # Attempt to decode content
            if response.headers.get("Content-Encoding") == "br":
                content = await response.read()  # Raw binary content
                try:
                    # Try Brotli decompression
                    content = brotli.decompress(content).decode("utf-8")
                except Exception as e:
                    # Fallback to reading response.text
                    content = await response.text()  # Await the text response
            else:
                # Use text content directly if not Brotli-encoded
                content = await response.text()

            # Parse JSON
            data = json.loads(content)
            return {
                "destination": destination,
                "prices": data,
            }
    except Exception as e:
        logger.error(f"Error fetching prices for {destination}: {e}")
        return {
            "destination": destination,
            "prices": None,
        }

async def fetch_prices_batch(
    origin: str, destinations: List[str], year_month: str, market: str
) -> List[Dict]:
    """
    Fetch prices for multiple destinations in parallel.
    """
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_prices(session, origin, destination, year_month, market)
            for destination in destinations
        ]
        return await asyncio.gather(*tasks)


def get_prices_in_batches(
    origin: str, destinations: List[str], year_month: str, market: str
) -> List[Dict]:
    """
    Wrapper function to execute the async batch fetching.
    """
    return asyncio.run(fetch_prices_batch(origin, destinations, year_month, market))