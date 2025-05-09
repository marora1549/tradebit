from unittest.mock import patch, MagicMock

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.models import UserSettings

User = get_user_model()


class ZerodhaAuthViewsTest(APITestCase):
    """
    Test suite for the Zerodha authentication views.
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
            zerodha_api_secret="test_api_secret"
        )
        
        # Setup the API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # URLs for testing
        self.login_url = reverse('zerodha-login')
        self.callback_url = reverse('zerodha-callback')

    @patch('zerodha.views.ZerodhaService.get_login_url')
    def test_login_view(self, mock_get_login_url):
        # Mock the login URL
        mock_get_login_url.return_value = "https://test-login-url.com"
        
        # Make the request
        response = self.client.get(self.login_url)
        
        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["login_url"], "https://test-login-url.com")
        mock_get_login_url.assert_called_once_with(self.user.id)

    @patch('zerodha.views.ZerodhaService.get_login_url')
    def test_login_view_no_credentials(self, mock_get_login_url):
        # Mock no login URL (no credentials)
        mock_get_login_url.return_value = None
        
        # Make the request
        response = self.client.get(self.login_url)
        
        # Check the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    @patch('zerodha.views.ZerodhaService.generate_session')
    def test_callback_view_success(self, mock_generate_session):
        # Mock successful session generation
        mock_generate_session.return_value = True
        
        # Make the request
        response = self.client.get(f"{self.callback_url}?request_token=test_token")
        
        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("success", response.data)
        self.assertTrue(response.data["success"])
        mock_generate_session.assert_called_once_with(self.user.id, "test_token")

    @patch('zerodha.views.ZerodhaService.generate_session')
    def test_callback_view_failure(self, mock_generate_session):
        # Mock failed session generation
        mock_generate_session.return_value = False
        
        # Make the request
        response = self.client.get(f"{self.callback_url}?request_token=test_token")
        
        # Check the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_callback_view_no_token(self):
        # Make the request without a token
        response = self.client.get(self.callback_url)
        
        # Check the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)


class ZerodhaHoldingsViewTest(APITestCase):
    """
    Test suite for the Zerodha holdings view.
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
        
        # Setup the API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # URLs for testing
        self.holdings_url = reverse('zerodha-holdings')
        self.sync_holdings_url = reverse('zerodha-sync-holdings')

    @patch('zerodha.views.ZerodhaService.get_client_for_user')
    def test_holdings_view(self, mock_get_client):
        # Mock the Zerodha client
        mock_client = MagicMock()
        mock_client.get_holdings.return_value = [
            MagicMock(
                tradingsymbol="RELIANCE",
                exchange="NSE",
                quantity=10,
                average_price=2100.5,
                last_price=2200.75,
                pnl=1002.5,
                product="CNC"
            ),
            MagicMock(
                tradingsymbol="INFY",
                exchange="NSE",
                quantity=5,
                average_price=1500.0,
                last_price=1600.0,
                pnl=500.0,
                product="CNC"
            )
        ]
        mock_get_client.return_value = mock_client
        
        # Make the request
        response = self.client.get(self.holdings_url)
        
        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["tradingsymbol"], "RELIANCE")
        self.assertEqual(response.data[1]["tradingsymbol"], "INFY")

    @patch('zerodha.views.ZerodhaService.get_client_for_user')
    def test_holdings_view_no_client(self, mock_get_client):
        # Mock no client available
        mock_get_client.return_value = None
        
        # Make the request
        response = self.client.get(self.holdings_url)
        
        # Check the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    @patch('zerodha.views.ZerodhaService.sync_holdings')
    def test_sync_holdings_view_success(self, mock_sync_holdings):
        # Mock successful sync
        mock_sync_holdings.return_value = {
            "success": True,
            "created": 2,
            "updated": 1,
            "skipped": 0,
            "total": 3
        }
        
        # Make the request
        response = self.client.post(self.sync_holdings_url)
        
        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["created"], 2)
        self.assertEqual(response.data["updated"], 1)
        mock_sync_holdings.assert_called_once_with(self.user.id)

    @patch('zerodha.views.ZerodhaService.sync_holdings')
    def test_sync_holdings_view_failure(self, mock_sync_holdings):
        # Mock failed sync
        mock_sync_holdings.return_value = {
            "success": False,
            "message": "Failed to sync holdings"
        }
        
        # Make the request
        response = self.client.post(self.sync_holdings_url)
        
        # Check the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])
        self.assertEqual(response.data["message"], "Failed to sync holdings")


class ZerodhaOrderViewTest(APITestCase):
    """
    Test suite for the Zerodha order view.
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
        
        # Setup the API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # URLs for testing
        self.orders_url = reverse('zerodha-orders')
        self.place_order_url = reverse('zerodha-place-order')

    @patch('zerodha.views.ZerodhaService.get_client_for_user')
    def test_orders_view(self, mock_get_client):
        # Mock the Zerodha client
        mock_client = MagicMock()
        mock_client.get_orders.return_value = [
            MagicMock(
                order_id="order1",
                exchange="NSE",
                tradingsymbol="RELIANCE",
                transaction_type="BUY",
                order_type="MARKET",
                quantity=10,
                price=None,
                status="COMPLETE",
                filled_quantity=10,
                pending_quantity=0,
                average_price=2100.5
            ),
            MagicMock(
                order_id="order2",
                exchange="NSE",
                tradingsymbol="INFY",
                transaction_type="SELL",
                order_type="LIMIT",
                quantity=5,
                price=1600.0,
                status="PENDING",
                filled_quantity=0,
                pending_quantity=5,
                average_price=None
            )
        ]
        mock_get_client.return_value = mock_client
        
        # Make the request
        response = self.client.get(self.orders_url)
        
        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["order_id"], "order1")
        self.assertEqual(response.data[1]["order_id"], "order2")

    @patch('zerodha.views.ZerodhaService.get_client_for_user')
    def test_orders_view_no_client(self, mock_get_client):
        # Mock no client available
        mock_get_client.return_value = None
        
        # Make the request
        response = self.client.get(self.orders_url)
        
        # Check the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    @patch('zerodha.views.ZerodhaService.place_order')
    def test_place_order_view_success(self, mock_place_order):
        # Mock successful order placement
        mock_place_order.return_value = {
            "success": True,
            "order_id": "test_order_id",
            "message": "Order placed successfully"
        }
        
        # Order data
        order_data = {
            "exchange": "NSE",
            "tradingsymbol": "RELIANCE",
            "transaction_type": "BUY",
            "quantity": 1,
            "product": "CNC",
            "order_type": "MARKET"
        }
        
        # Make the request
        response = self.client.post(self.place_order_url, order_data, format="json")
        
        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["order_id"], "test_order_id")
        mock_place_order.assert_called_once_with(self.user.id, order_data)

    @patch('zerodha.views.ZerodhaService.place_order')
    def test_place_order_view_failure(self, mock_place_order):
        # Mock failed order placement
        mock_place_order.return_value = {
            "success": False,
            "message": "Failed to place order"
        }
        
        # Order data
        order_data = {
            "exchange": "NSE",
            "tradingsymbol": "RELIANCE",
            "transaction_type": "BUY",
            "quantity": 1,
            "product": "CNC",
            "order_type": "MARKET"
        }
        
        # Make the request
        response = self.client.post(self.place_order_url, order_data, format="json")
        
        # Check the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])
        self.assertEqual(response.data["message"], "Failed to place order")

    def test_place_order_view_invalid_data(self):
        # Invalid order data (missing required fields)
        order_data = {
            "exchange": "NSE",
            "tradingsymbol": "RELIANCE"
            # Missing other required fields
        }
        
        # Make the request
        response = self.client.post(self.place_order_url, order_data, format="json")
        
        # Check the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("transaction_type", response.data)
        self.assertIn("quantity", response.data)
        self.assertIn("product", response.data)
        self.assertIn("order_type", response.data)
