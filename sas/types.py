from typing import TypedDict


class Flight(TypedDict):
    cityName: str
    countryName: str
    airportName: str
    outBoundDate: str
    inBoundDate: str
    marketTotalPrice: float
    url: str


class Trip(TypedDict):
    region: str
    flights: Flight
