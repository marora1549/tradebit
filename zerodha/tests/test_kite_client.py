from datetime import datetime
from unittest.mock import patch, MagicMock

from django.test import TestCase
from zerodha.kite_client import KiteClient, ZerodhaException, KiteHolding


class KiteClientTest(TestCase):
    """
    Test suite for the KiteClient class.
    """
    def setUp(self):
        self.api_key = "test_api_key"
        self.api_secret = "test_api_secret"
        self.access_token = "test_access_token"
        self.client = KiteClient(
            api_key=self.api_key,
            api_secret=self.api_secret,
            access_token=self.access_token
        )
    
    def test_initialization(self):
        self.assertEqual(self.client.api_key, self.api_key)
        self.assertEqual(self.client.api_secret, self.api_secret)
        self.assertEqual(self.client.access_token, self.access_token)
    
    def test_get_login_url(self):
        login_url = self.client.get_login_url()
        expected_url = f"https://kite.zerodha.com/connect/login?api_key={self.api_key}&v=3"
        self.assertEqual(login_url, expected_url)
    
    @patch("zerodha.kite_client.requests.Session.request")
    def test_make_request_success(self, mock_request):
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success", "data": {"key": "value"}}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        # Make the request
        result = self.client._make_request("GET", "/test/endpoint")
        
        # Check the result
        self.assertEqual(result, {"key": "value"})
        
        # Verify the request was made correctly
        mock_request.assert_called_once_with(
            method="GET",
            url="https://api.kite.trade/test/endpoint",
            params=None,
            data=None,
            headers={"Authorization": f"Token {self.api_key}:{self.access_token}"},
            timeout=10
        )
    
    @patch("zerodha.kite_client.requests.Session.request")
    def test_make_request_api_error(self, mock_request):
        # Mock the response with an API error
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "error", "message": "Test error message"}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        # Test that an exception is raised
        with self.assertRaises(ZerodhaException) as context:
            self.client._make_request("GET", "/test/endpoint")
        
        self.assertIn("Test error message", str(context.exception))
    
    @patch("zerodha.kite_client.requests.Session.request")
    def test_generate_session(self, mock_request):
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "success",
            "data": {
                "access_token": "new_access_token",
                "refresh_token": "refresh_token"
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        # Call the method
        result = self.client.generate_session("test_request_token")
        
        # Check the result
        self.assertEqual(result["access_token"], "new_access_token")
        self.assertEqual(result["refresh_token"], "refresh_token")
        self.assertIsInstance(result["session_expiry"], datetime)
        
        # Verify that the access token was updated
        self.assertEqual(self.client.access_token, "new_access_token")
    
    @patch("zerodha.kite_client.KiteClient._make_request")
    def test_get_holdings(self, mock_make_request):
        # Mock the holdings data
        mock_holdings_data = [
            {
                "tradingsymbol": "RELIANCE",
                "exchange": "NSE",
                "isin": "INE002A01018",
                "quantity": 10,
                "average_price": 2100.5,
                "last_price": 2200.75,
                "pnl": 1002.5,
                "product": "CNC"
            },
            {
                "tradingsymbol": "INFY",
                "exchange": "NSE",
                "isin": "INE009A01021",
                "quantity": 5,
                "average_price": 1500.0,
                "last_price": 1600.0,
                "pnl": 500.0,
                "product": "CNC"
            }
        ]
        mock_make_request.return_value = mock_holdings_data
        
        # Call the method
        holdings = self.client.get_holdings()
        
        # Check the result
        self.assertEqual(len(holdings), 2)
        self.assertIsInstance(holdings[0], KiteHolding)
        self.assertEqual(holdings[0].tradingsymbol, "RELIANCE")
        self.assertEqual(holdings[0].quantity, 10)
        self.assertEqual(holdings[1].tradingsymbol, "INFY")
        self.assertEqual(holdings[1].average_price, 1500.0)
        
        # Verify the request was made correctly
        mock_make_request.assert_called_once_with("GET", "/portfolio/holdings")
    
    @patch("zerodha.kite_client.KiteClient._make_request")
    def test_place_order(self, mock_make_request):
        # Mock the order response
        mock_make_request.return_value = {"order_id": "test_order_id"}
        
        # Call the method
        order_id = self.client.place_order(
            exchange="NSE",
            tradingsymbol="RELIANCE",
            transaction_type="BUY",
            quantity=1,
            product="CNC",
            order_type="MARKET"
        )
        
        # Check the result
        self.assertEqual(order_id, "test_order_id")
        
        # Verify the request was made correctly
        mock_make_request.assert_called_once_with(
            "POST", 
            "/orders/regular", 
            data={
                "exchange": "NSE",
                "tradingsymbol": "RELIANCE",
                "transaction_type": "BUY",
                "quantity": 1,
                "product": "CNC",
                "order_type": "MARKET",
                "validity": "DAY",
                "disclosed_quantity": 0.0,
            }
        )
