import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union

import requests
from django.conf import settings
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class KiteCredentials(BaseModel):
    """
    Pydantic model for Zerodha Kite API credentials.
    """
    api_key: str
    api_secret: str
    request_token: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    session_expiry: Optional[datetime] = None


class KiteHolding(BaseModel):
    """
    Pydantic model for a holding from Zerodha Kite API.
    """
    tradingsymbol: str
    exchange: str
    isin: Optional[str] = None
    quantity: float
    average_price: float
    last_price: float
    pnl: float
    day_change: Optional[float] = 0.0
    day_change_percentage: Optional[float] = 0.0
    product: str = Field(..., description="CNC, MIS, etc.")


class KiteOrder(BaseModel):
    """
    Pydantic model for an order from Zerodha Kite API.
    """
    order_id: str
    exchange: str
    tradingsymbol: str
    transaction_type: str
    order_type: str
    quantity: float
    price: Optional[float] = None
    status: str
    filled_quantity: float = 0.0
    pending_quantity: float = 0.0
    average_price: Optional[float] = None
    order_timestamp: Optional[datetime] = None
    exchange_timestamp: Optional[datetime] = None


class ZerodhaException(Exception):
    """
    Exception raised for errors in the Zerodha API.
    """
    pass


class KiteClient:
    """
    Client for interacting with the Zerodha Kite API.
    """
    BASE_URL = "https://api.kite.trade"
    LOGIN_URL = "https://kite.zerodha.com/connect/login"
    
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        api_secret: Optional[str] = None,
        access_token: Optional[str] = None
    ):
        """
        Initialize the Kite API client.
        
        Args:
            api_key: The API key issued by Zerodha
            api_secret: The API secret issued by Zerodha
            access_token: Access token for authentication (optional)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self._session = requests.Session()
        
        # Add a default user agent
        self._session.headers.update({
            "X-Kite-Version": "3",
            "User-Agent": "TradeBit/1.0"
        })
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict] = None, 
        data: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Dict:
        """
        Make a request to the Kite API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint to request
            params: URL parameters
            data: Request body for POST/PUT requests
            headers: Additional headers
            
        Returns:
            Parsed JSON response as dictionary
            
        Raises:
            ZerodhaException: If the API returns an error
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        # Set default headers
        request_headers = {}
        if self.access_token:
            request_headers["Authorization"] = f"Token {self.api_key}:{self.access_token}"
        
        # Update with any additional headers
        if headers:
            request_headers.update(headers)
        
        try:
            response = self._session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                headers=request_headers,
                timeout=10  # 10 second timeout
            )
            
            # Raise exception if status code indicates an error
            response.raise_for_status()
            
            json_response = response.json()
            
            # Zerodha API returns errors even with 200 status codes sometimes
            if json_response.get("status") == "error":
                raise ZerodhaException(
                    f"Zerodha API Error: {json_response.get('message', 'Unknown error')}"
                )
                
            return json_response["data"] if "data" in json_response else json_response
            
        except requests.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            raise ZerodhaException(f"Request failed: {str(e)}")
        except ValueError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            raise ZerodhaException(f"Failed to parse response: {str(e)}")
    
    def get_login_url(self) -> str:
        """
        Generate the login URL for Zerodha authorization.
        
        Returns:
            URL to redirect the user for authentication
        """
        return f"{self.LOGIN_URL}?api_key={self.api_key}&v=3"
    
    def generate_session(
        self, request_token: str
    ) -> Dict[str, Union[str, datetime]]:
        """
        Generate a session using the request token obtained from the redirect.
        
        Args:
            request_token: Request token received from the redirect URL
            
        Returns:
            Dictionary with access_token, refresh_token, and expiry
            
        Raises:
            ZerodhaException: If session generation fails
        """
        try:
            data = {
                "api_key": self.api_key,
                "request_token": request_token,
                "checksum": self.api_secret
            }
            
            response = self._make_request(
                method="POST",
                endpoint="/session/token",
                data=data
            )
            
            # Update the client with the access token
            self.access_token = response.get("access_token")
            
            # Calculate expiry time (Zerodha tokens expire at 6 AM the next day)
            now = datetime.now()
            tomorrow = now + timedelta(days=1)
            expiry = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 6, 0, 0)
            
            return {
                "access_token": response.get("access_token"),
                "refresh_token": response.get("refresh_token"),
                "session_expiry": expiry
            }
            
        except Exception as e:
            logger.error(f"Session generation error: {str(e)}")
            raise ZerodhaException(f"Failed to generate session: {str(e)}")
    
    def get_profile(self) -> Dict:
        """
        Get user profile details.
        
        Returns:
            User profile data
            
        Raises:
            ZerodhaException: If profile retrieval fails
        """
        return self._make_request("GET", "/user/profile")
    
    def get_holdings(self) -> List[KiteHolding]:
        """
        Get user's holdings.
        
        Returns:
            List of holdings
            
        Raises:
            ZerodhaException: If holdings retrieval fails
        """
        try:
            holdings_data = self._make_request("GET", "/portfolio/holdings")
            return [KiteHolding(**holding) for holding in holdings_data]
        except Exception as e:
            logger.error(f"Error fetching holdings: {str(e)}")
            raise ZerodhaException(f"Failed to get holdings: {str(e)}")
    
    def get_positions(self) -> Dict:
        """
        Get user's positions.
        
        Returns:
            Dictionary with day and net positions
            
        Raises:
            ZerodhaException: If positions retrieval fails
        """
        return self._make_request("GET", "/portfolio/positions")
    
    def place_order(
        self,
        exchange: str,
        tradingsymbol: str,
        transaction_type: str,  # BUY or SELL
        quantity: float,
        product: str,  # CNC, MIS, etc.
        order_type: str,  # MARKET, LIMIT, etc.
        price: Optional[float] = None,
        trigger_price: Optional[float] = None,
        validity: str = "DAY",
        disclosed_quantity: float = 0.0,
        squareoff: Optional[float] = None,
        stoploss: Optional[float] = None,
        trailing_stoploss: Optional[float] = None,
        tag: Optional[str] = None
    ) -> str:
        """
        Place an order on Zerodha.
        
        Args:
            exchange: Exchange to trade on (NSE, BSE, etc.)
            tradingsymbol: Trading symbol of the instrument
            transaction_type: BUY or SELL
            quantity: Quantity to transact
            product: Product code (CNC, MIS, etc.)
            order_type: Order type (MARKET, LIMIT, etc.)
            price: Price for LIMIT orders
            trigger_price: Trigger price for SL, SL-M orders
            validity: Order validity (DAY, IOC, etc.)
            disclosed_quantity: Quantity to disclose for partial fills
            squareoff: Square off value for bracket orders
            stoploss: Stoploss value for bracket orders
            trailing_stoploss: Trailing stoploss for bracket orders
            tag: User tag for the order
            
        Returns:
            Order ID
            
        Raises:
            ZerodhaException: If order placement fails
        """
        try:
            params = {
                "exchange": exchange,
                "tradingsymbol": tradingsymbol,
                "transaction_type": transaction_type,
                "quantity": quantity,
                "product": product,
                "order_type": order_type,
                "validity": validity,
                "disclosed_quantity": disclosed_quantity,
            }
            
            # Add optional parameters if provided
            if price is not None:
                params["price"] = price
                
            if trigger_price is not None:
                params["trigger_price"] = trigger_price
                
            if squareoff is not None:
                params["squareoff"] = squareoff
                
            if stoploss is not None:
                params["stoploss"] = stoploss
                
            if trailing_stoploss is not None:
                params["trailing_stoploss"] = trailing_stoploss
                
            if tag is not None:
                params["tag"] = tag
            
            response = self._make_request("POST", "/orders/regular", data=params)
            return response.get("order_id")
            
        except Exception as e:
            logger.error(f"Order placement error: {str(e)}")
            raise ZerodhaException(f"Failed to place order: {str(e)}")
    
    def get_orders(self) -> List[KiteOrder]:
        """
        Get list of orders.
        
        Returns:
            List of orders
            
        Raises:
            ZerodhaException: If order retrieval fails
        """
        try:
            orders_data = self._make_request("GET", "/orders")
            return [KiteOrder(**order) for order in orders_data]
        except Exception as e:
            logger.error(f"Error fetching orders: {str(e)}")
            raise ZerodhaException(f"Failed to get orders: {str(e)}")
    
    def get_order_history(self, order_id: str) -> List[Dict]:
        """
        Get history of an order.
        
        Args:
            order_id: ID of the order to fetch history for
            
        Returns:
            List of order statuses
            
        Raises:
            ZerodhaException: If order history retrieval fails
        """
        return self._make_request("GET", f"/orders/{order_id}")
    
    def get_instruments(self, exchange: Optional[str] = None) -> List[Dict]:
        """
        Get list of instruments available to trade.
        
        Args:
            exchange: Optional filter by exchange (NSE, BSE, etc.)
            
        Returns:
            List of instruments
            
        Raises:
            ZerodhaException: If instrument retrieval fails
        """
        endpoint = "/instruments"
        if exchange:
            endpoint += f"/{exchange}"
            
        return self._make_request("GET", endpoint)
    
    def get_quote(self, *instruments: str) -> Dict:
        """
        Get quotes for instruments.
        
        Args:
            instruments: List of instruments in the format 'exchange:tradingsymbol'
            
        Returns:
            Dictionary of quotes indexed by the instrument
            
        Raises:
            ZerodhaException: If quote retrieval fails
        """
        params = {"i": instruments}
        return self._make_request("GET", "/quote", params=params)
    
    def is_session_valid(self) -> bool:
        """
        Check if the current session is valid.
        
        Returns:
            True if session is valid, False otherwise
        """
        if not self.access_token:
            return False
            
        try:
            # A lightweight API call to check session validity
            self._make_request("GET", "/user/margins")
            return True
        except Exception:
            return False
