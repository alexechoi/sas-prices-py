from typing import List, Dict
from sas.data import regions
from sas.sas_monthly import get_monthly_round_trip_prices
from sas.sas_cheapest import get_cheapest_round_trips
from sas.sas_batch import get_prices_in_batches
import logging
from datetime import datetime, timedelta
import requests

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SAS:
    def __init__(self, market: str = "gb-en"):
        self.market = market

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
            origin (str): Origin airport code. Required.

        Returns:
            List[Dict]: A list of the cheapest trips or an empty list if no trips are found.
        """
        if not origin:
            raise ValueError("The 'origin' parameter is required and cannot be None.")

        if not start_date:
            start_date = datetime.now().strftime("%Y-%m-%d")
            logger.info(f"No start date provided. Using today's date: {start_date}")

        if region:
            if region not in regions:
                logger.error(f"Invalid region: {region}. Available regions: {', '.join(regions.keys())}")
                return []
            destinations = regions[region]

        else:
            # Combine all destinations across all regions
            destinations = ",".join(dest for dest in regions.values())

        return get_cheapest_round_trips(
            market=self.market,
            origin=origin,
            destinations=destinations,
            start_date=start_date,
        )

    def get_monthly_round_trips(self, origin: str, destination: str, year_month: str) -> List[Dict]:
        """
        Get monthly round trip prices for a specific origin-destination pair.

        Args:
            origin (str): Origin airport code.
            destination (str): Destination airport code.
            year_month (str): Year and return month in the format "YYYYMM,YYYYMM".

        Returns:
            List[Dict]: List of dates with round trip prices.
        """
        return get_monthly_round_trip_prices(origin, destination, year_month, market=self.market)

    def get_cheapest_trips_by_length(
        self,
        origin: str,
        destination: str,
        year_month: str,
        trip_length: int,
    ) -> List[Dict]:
        """
        Get the cheapest round trips for a specific origin-destination pair and trip length.

        Args:
            origin (str): Origin airport code.
            destination (str): Destination airport code.
            year_month (str): Year and return month in the format "YYYYMM,YYYYMM".
            trip_length (int): Desired trip length in days.

        Returns:
            List[Dict]: List of cheapest round trips matching the given trip length.
        """
        monthly_trips = self.get_monthly_round_trips(origin=origin, destination=destination, year_month=year_month)

        if not monthly_trips:
            logger.warning("No monthly trips found for the given origin and destination.")
            return []

        # Parse and filter trips by trip length
        round_trip_prices = []
        for trip in monthly_trips:
            try:
                out_date = datetime.strptime(trip["outbound_date"], "%Y%m%d")
                in_date = datetime.strptime(trip["inbound_date"], "%Y%m%d")
                if (in_date - out_date).days == trip_length:
                    round_trip_prices.append(trip)
            except Exception as e:
                logger.warning(f"Error processing trip: {trip}. Error: {e}")

        return sorted(round_trip_prices, key=lambda x: x["round_trip_price"])

    def get_cheapest_trips_by_length_all_destinations(
        self,
        origin: str,
        year_month: str,
        trip_length: int,
        regions_to_search: List[str] = None,
    ) -> List[Dict]:
        """
        Get the cheapest round trips for a given origin and trip length across all destinations.
        """
        if not regions_to_search:
            regions_to_search = regions.keys()

        all_destinations = []
        for region_name in regions_to_search:
            all_destinations.extend(regions[region_name].split(","))

        logger.info(f"Fetching prices for {len(all_destinations)} destinations in parallel.")
        results = get_prices_in_batches(origin, all_destinations, year_month, self.market)

        all_trips = []
        for result in results:
            destination = result["destination"]
            prices = result["prices"]
            if not prices:
                continue

            outbound = prices.get("outbound", {})
            inbound = prices.get("inbound", {})

            # Filter trips by desired length
            for out_date, out_price in outbound.items():
                for in_date, in_price in inbound.items():
                    try:
                        out_date_obj = datetime.strptime(out_date, "%Y%m%d")
                        in_date_obj = datetime.strptime(in_date, "%Y%m%d")
                        if (in_date_obj - out_date_obj).days == trip_length:
                            all_trips.append({
                                "destination": destination,
                                "outbound_date": out_date,
                                "inbound_date": in_date,
                                "round_trip_price": out_price["totalPrice"] + in_price["totalPrice"],
                            })
                    except Exception as e:
                        logger.warning(f"Error processing trip for {destination}: {e}")

        return sorted(all_trips, key=lambda x: x["round_trip_price"])