from datetime import datetime


def parse_date(date_str: str) -> datetime:
    """Parse a date string into a datetime object."""
    return datetime.strptime(date_str, "%Y-%m-%d")