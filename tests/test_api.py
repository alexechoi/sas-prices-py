import unittest
from unittest.mock import patch, Mock
from sas.api import SAS
from sas.data import regions


class TestSASAPI(unittest.TestCase):
    def setUp(self):
        """Set up common test data."""
        self.sas = SAS()
        self.mock_start_date = "2024-11-25"

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
        mock_response.text = "Internal Server Error"  # Add this
        return mock_response

    @patch("sas.api.requests.get")
    def test_get_cheapest_round_trips_europe(self, mock_get):
        """Test fetching cheapest round trips for the Europe region."""
        mock_get.return_value = self.mock_success_response()

        trips = self.sas.get_cheapest_round_trips(regions["Europe"], self.mock_start_date)

        # Assertions
        self.assertIsInstance(trips, list)
        self.assertGreaterEqual(len(trips), 1)
        self.assertIn("cityName", trips[0])
        self.assertEqual(trips[0]["cityName"], "Oslo")

    @patch("sas.api.requests.get")
    def test_get_cheapest_round_trips_nordics(self, mock_get):
        """Test fetching cheapest round trips for the Nordics region."""
        mock_get.return_value = self.mock_success_response()

        trips = self.sas.get_cheapest_round_trips(regions["Nordics"], self.mock_start_date)

        # Assertions
        self.assertIsInstance(trips, list)
        self.assertGreaterEqual(len(trips), 1)
        self.assertIn("cityName", trips[0])
        self.assertEqual(trips[0]["cityName"], "Oslo")

    @patch("sas.api.requests.get")
    def test_get_cheapest_round_trips_all_destinations(self, mock_get):
        """Test fetching cheapest round trips for all destinations combined."""
        all_destinations = ",".join(regions.values())
        mock_get.return_value = self.mock_success_response()

        trips = self.sas.get_cheapest_round_trips(all_destinations, self.mock_start_date)

        # Assertions
        self.assertIsInstance(trips, list)
        self.assertGreaterEqual(len(trips), 1)
        self.assertIn("cityName", trips[0])
        self.assertEqual(trips[0]["cityName"], "Oslo")

    @patch("sas.api.requests.get")
    def test_api_failure_handling(self, mock_get):
        """Test API failure response."""
        mock_get.return_value = self.mock_failure_response()

        trips = self.sas.get_cheapest_round_trips(regions["Asia"], self.mock_start_date)

        # Assertions
        self.assertEqual(trips, [])

    @patch("sas.api.requests.get")
    def test_invalid_data_handling(self, mock_get):
        """Test handling of invalid or corrupted data."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Encoding": "application/json"}
        mock_response.text = '{"invalid_key": "no_prices"}'  # Invalid structure
        mock_get.return_value = mock_response

        trips = self.sas.get_cheapest_round_trips(regions["Africa"], self.mock_start_date)

        # Assertions
        self.assertEqual(trips, [])

    @patch("sas.api.requests.get")
    def test_empty_response_handling(self, mock_get):
        """Test handling of an empty API response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Encoding": "application/json"}
        mock_response.text = "[]"  # No trips available
        mock_get.return_value = mock_response

        trips = self.sas.get_cheapest_round_trips(regions["North America"], self.mock_start_date)

        # Assertions
        self.assertIsInstance(trips, list)
        self.assertEqual(len(trips), 0)

if __name__ == "__main__":
    unittest.main()