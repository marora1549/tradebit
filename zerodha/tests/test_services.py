from unittest.mock import patch, MagicMock
from datetime import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Stock
from portfolio.models import Holding
from users.models import UserSettings
from zerodha.services import ZerodhaService
from zerodha.kite_client import KiteHolding

User = get_user_model()


class ZerodhaServiceTest(TestCase):
    """
    Test suite for the ZerodhaService class.
    """
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        
        # Create user settings with Zerodha credentials
        self.user_settings = UserSettings.objects.create(
            user=self.user,
            zerodha_api_key="test_api_key",
            zerodha_api_secret="test_api_secret",
            zerodha_access_token="test_access_token"
        )
        
        # Create some test stocks
        self.stock1 = Stock.objects.create(
            symbol="RELIANCE",
            name="Reliance Industries Ltd.",
            sector="Energy",
            industry="Oil & Gas"
        )
        
        self.stock2 = Stock.objects.create(
            symbol="INFY",
            name="Infosys Ltd.",
            sector="Technology",
            industry="IT Services"
        )
    
    @patch("zerodha.services.KiteClient")
    def test_get_client_for_user(self, MockKiteClient):
        # Mock the KiteClient
        mock_client = MagicMock()
        mock_client.is_session_valid.return_value = True
        MockKiteClient.return_value = mock_client
        
        # Call the method
        client = ZerodhaService.get_client_for_user(self.user.id)
        
        # Check that the client was created correctly
        MockKiteClient.assert_called_once_with(
            api_key="test_api_key",
            api_secret="test_api_secret",
            access_token="test_access_token"
        )
        
        # Check that the client was returned
        self.assertEqual(client, mock_client)
    
    @patch("zerodha.services.KiteClient")
    def test_get_client_no_credentials(self, MockKiteClient):
        # Remove credentials
        self.user_settings.zerodha_api_key = None
        self.user_settings.zerodha_api_secret = None
        self.user_settings.save()
        
        # Call the method
        client = ZerodhaService.get_client_for_user(self.user.id)
        
        # Check that no client was returned
        self.assertIsNone(client)
        MockKiteClient.assert_not_called()
    
    @patch("zerodha.services.ZerodhaService.get_client_for_user")
    def test_get_login_url(self, mock_get_client):
        # Mock the client
        mock_client = MagicMock()
        mock_client.get_login_url.return_value = "https://test-login-url.com"
        mock_get_client.return_value = mock_client
        
        # Call the method
        login_url = ZerodhaService.get_login_url(self.user.id)
        
        # Check the result
        self.assertEqual(login_url, "https://test-login-url.com")
        mock_get_client.assert_called_once_with(self.user.id)
        mock_client.get_login_url.assert_called_once()
    
    @patch("zerodha.services.ZerodhaService.get_client_for_user")
    def test_generate_session(self, mock_get_client):
        # Mock the client
        mock_client = MagicMock()
        mock_client.generate_session.return_value = {
            "access_token": "new_access_token",
            "refresh_token": "new_refresh_token",
            "session_expiry": datetime.now()
        }
        mock_get_client.return_value = mock_client
        
        # Call the method
        result = ZerodhaService.generate_session(
            user_id=self.user.id,
            request_token="test_request_token"
        )
        
        # Check the result
        self.assertTrue(result)
        mock_get_client.assert_called_once_with(self.user.id)
        mock_client.generate_session.assert_called_once_with("test_request_token")
        
        # Verify that the user settings were updated
        self.user_settings.refresh_from_db()
        self.assertEqual(self.user_settings.zerodha_request_token, "test_request_token")
        self.assertEqual(self.user_settings.zerodha_access_token, "new_access_token")
        self.assertEqual(self.user_settings.zerodha_refresh_token, "new_refresh_token")
        self.assertIsNotNone(self.user_settings.zerodha_session_expiry)
    
    @patch("zerodha.services.ZerodhaService.get_client_for_user")
    def test_sync_holdings(self, mock_get_client):
        # Create mock holdings data
        mock_holdings = [
            KiteHolding(
                tradingsymbol="RELIANCE",
                exchange="NSE",
                isin="INE002A01018",
                quantity=10,
                average_price=2100.5,
                last_price=2200.75,
                pnl=1002.5,
                product="CNC"
            ),
            KiteHolding(
                tradingsymbol="INFY",
                exchange="NSE",
                isin="INE009A01021",
                quantity=5,
                average_price=1500.0,
                last_price=1600.0,
                pnl=500.0,
                product="CNC"
            ),
            KiteHolding(
                tradingsymbol="NEWSTOCK",  # This one doesn't exist in our test data
                exchange="NSE",
                isin="INE123X01099",
                quantity=3,
                average_price=100.0,
                last_price=110.0,
                pnl=30.0,
                product="CNC"
            )
        ]
        
        # Mock the client
        mock_client = MagicMock()
        mock_client.get_holdings.return_value = mock_holdings
        mock_get_client.return_value = mock_client
        
        # Call the method
        result = ZerodhaService.sync_holdings(self.user.id)
        
        # Check the result
        self.assertTrue(result["success"])
        self.assertEqual(result["total"], 3)
        
        # Verify that holdings were created
        holdings = Holding.objects.filter(user=self.user).order_by('stock__symbol')
        self.assertEqual(holdings.count(), 3)
        
        # Check the holdings data
        self.assertEqual(holdings[0].stock.symbol, "INFY")
        self.assertEqual(holdings[0].quantity, 5)
        self.assertEqual(holdings[0].avg_price, 1500.0)
        self.assertEqual(holdings[0].source, "zerodha")
        
        self.assertEqual(holdings[1].stock.symbol, "NEWSTOCK")
        self.assertEqual(holdings[1].quantity, 3)
        self.assertEqual(holdings[1].avg_price, 100.0)
        
        self.assertEqual(holdings[2].stock.symbol, "RELIANCE")
        self.assertEqual(holdings[2].quantity, 10)
        self.assertEqual(holdings[2].avg_price, 2100.5)
    
    @patch("zerodha.services.ZerodhaService.get_client_for_user")
    def test_place_order(self, mock_get_client):
        # Mock the client
        mock_client = MagicMock()
        mock_client.place_order.return_value = "test_order_id"
        mock_get_client.return_value = mock_client
        
        # Call the method
        order_data = {
            "exchange": "NSE",
            "tradingsymbol": "RELIANCE",
            "transaction_type": "BUY",
            "quantity": 1,
            "product": "CNC",
            "order_type": "MARKET"
        }
        result = ZerodhaService.place_order(self.user.id, order_data)
        
        # Check the result
        self.assertTrue(result["success"])
        self.assertEqual(result["order_id"], "test_order_id")
        self.assertEqual(result["message"], "Order placed successfully")
        
        # Verify that the order was placed correctly
        mock_get_client.assert_called_once_with(self.user.id)
        mock_client.place_order.assert_called_once_with(**order_data)
