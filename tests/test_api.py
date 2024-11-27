import unittest
from unittest.mock import patch, Mock
from sas.api import SAS
from sas.data import regions


class TestSASAPI(unittest.TestCase):
    def setUp(self):
        """Set up common test data."""
        self.sas = SAS()
        self.mock_start_date = "2024-11-25"
        self.mock_year_month = "202501,202501"

    def mock_success_response(self, content=None):
        """Create a mock response simulating successful data."""
        if content is None:
            content = (
                '[{"countryName": "Norway", "cityName": "Oslo", "airportName": "Gardermoen", '
                '"prices": [{"outBoundDate": "2024-11-30", "inBoundDate": "2024-12-05", '
                '"lowestPrice": {"marketTotalPrice": 300.0}}]}]'
            )
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Encoding": "application/json"}
        mock_response.text = content
        return mock_response

    def mock_failure_response(self):
        """Create a mock response simulating an API failure."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        return mock_response

    @patch("sas.sas_cheapest.requests.get")
    def test_get_cheapest_round_trips_europe(self, mock_get):
        """Test fetching cheapest round trips for the Europe region."""
        mock_get.return_value = self.mock_success_response()

        trips = self.sas.get_cheapest_round_trips(region="Europe", origin="LHR")

        # Assertions
        self.assertIsInstance(trips, list)
        self.assertGreaterEqual(len(trips), 1)
        self.assertIn("cityName", trips[0])
        self.assertIn("prices", trips[0])

    @patch("sas.sas_monthly.requests.get")
    def test_get_cheapest_trips_by_length(self, mock_get):
        """Test fetching cheapest trips by length for a specific destination."""
        content = (
            '{"outbound": {"20250101": {"totalPrice": 69.32}}, '
            '"inbound": {"20250103": {"totalPrice": 89.99}}}'
        )
        mock_get.return_value = self.mock_success_response(content)

        trips = self.sas.get_cheapest_trips_by_length(
            origin="LHR", destination="CPH", year_month=self.mock_year_month, trip_length=2
        )

        # Assertions
        self.assertIsInstance(trips, list)
        self.assertGreaterEqual(len(trips), 1)
        self.assertIn("outbound_date", trips[0])
        self.assertIn("round_trip_price", trips[0])

    @patch("sas.sas_monthly.requests.get")
    def test_get_cheapest_trips_by_length_all_destinations(self, mock_get):
        """Test fetching cheapest trips by length across all destinations."""
        content = (
            '{"outbound": {"20250101": {"totalPrice": 70.00}}, '
            '"inbound": {"20250103": {"totalPrice": 63.82}}}'
        )
        mock_get.return_value = self.mock_success_response(content)

        trips = self.sas.get_cheapest_trips_by_length_all_destinations(
            origin="LHR", year_month=self.mock_year_month, trip_length=2, regions_to_search=["Europe"]
        )

        # Assertions
        self.assertIsInstance(trips, list)
        self.assertGreaterEqual(len(trips), 1)
        self.assertIn("destination", trips[0])
        self.assertIn("round_trip_price", trips[0])
        self.assertIsInstance(trips[0]["round_trip_price"], float)

    @patch("sas.sas_cheapest.requests.get")
    def test_empty_response_handling(self, mock_get):
        """Test handling of an empty API response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Encoding": "application/json"}
        mock_response.text = "[]"  # No trips available
        mock_get.return_value = mock_response

        trips = self.sas.get_cheapest_round_trips(region="Asia", origin="LHR")

        # Assertions
        self.assertIsInstance(trips, list)
        self.assertEqual(len(trips), 0)

    @patch("sas.sas_cheapest.requests.get")
    def test_api_failure_handling(self, mock_get):
        """Test handling of API failure responses."""
        mock_get.return_value = self.mock_failure_response()

        trips = self.sas.get_cheapest_round_trips(region="North America", origin="LHR")

        # Assertions
        self.assertEqual(trips, [])

if __name__ == "__main__":
    unittest.main()