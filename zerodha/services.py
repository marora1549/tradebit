import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

from django.contrib.auth import get_user_model
from django.db import transaction

from core.models import Stock, StockAlias
from portfolio.models import Holding
from users.models import UserSettings
from zerodha.kite_client import KiteClient, KiteHolding, ZerodhaException

User = get_user_model()
logger = logging.getLogger(__name__)


class ZerodhaService:
    """
    Service class for Zerodha operations.
    """
    @staticmethod
    def get_client_for_user(user_id: int) -> Optional[KiteClient]:
        """
        Get a configured Kite client for the specified user.
        
        Args:
            user_id: ID of the user to get client for
            
        Returns:
            Configured KiteClient instance or None if credentials not available
        """
        try:
            user_settings = UserSettings.objects.get(user_id=user_id)
            
            # Check if we have the required credentials
            if not user_settings.zerodha_api_key or not user_settings.zerodha_api_secret:
                logger.warning(f"Zerodha API credentials not configured for user {user_id}")
                return None
            
            # Create client with credentials
            client = KiteClient(
                api_key=user_settings.zerodha_api_key,
                api_secret=user_settings.zerodha_api_secret,
                access_token=user_settings.zerodha_access_token
            )
            
            # Check if the session is valid
            if user_settings.zerodha_access_token and client.is_session_valid():
                return client
            else:
                logger.info(f"Zerodha session invalid for user {user_id}")
                return client  # Return client without valid session
                
        except UserSettings.DoesNotExist:
            logger.error(f"UserSettings not found for user {user_id}")
            return None
        except Exception as e:
            logger.error(f"Error creating Zerodha client for user {user_id}: {str(e)}")
            return None
    
    @staticmethod
    def get_login_url(user_id: int) -> Optional[str]:
        """
        Get the Zerodha login URL for the specified user.
        
        Args:
            user_id: ID of the user to get login URL for
            
        Returns:
            Login URL or None if credentials not available
        """
        client = ZerodhaService.get_client_for_user(user_id)
        if client:
            return client.get_login_url()
        return None
    
    @staticmethod
    def generate_session(user_id: int, request_token: str) -> bool:
        """
        Generate a Zerodha session for the specified user using the request token.
        
        Args:
            user_id: ID of the user to generate session for
            request_token: Request token from Zerodha redirect
            
        Returns:
            True if session was successfully generated, False otherwise
        """
        try:
            client = ZerodhaService.get_client_for_user(user_id)
            if not client:
                return False
            
            # Generate session with the request token
            session_data = client.generate_session(request_token)
            
            # Update user settings with the session data
            user_settings = UserSettings.objects.get(user_id=user_id)
            user_settings.zerodha_request_token = request_token
            user_settings.zerodha_access_token = session_data.get("access_token")
            user_settings.zerodha_refresh_token = session_data.get("refresh_token")
            user_settings.zerodha_session_expiry = session_data.get("session_expiry")
            user_settings.save()
            
            return True
            
        except Exception as e:
            logger.error(f"Error generating Zerodha session for user {user_id}: {str(e)}")
            return False
    
    @staticmethod
    def sync_holdings(user_id: int) -> Dict[str, Any]:
        """
        Sync holdings from Zerodha to the local database.
        
        Args:
            user_id: ID of the user to sync holdings for
            
        Returns:
            Dictionary with sync results
        """
        try:
            client = ZerodhaService.get_client_for_user(user_id)
            if not client:
                return {"success": False, "message": "Zerodha client not available"}
            
            # Get holdings from Zerodha
            zerodha_holdings = client.get_holdings()
            
            user = User.objects.get(id=user_id)
            
            # Start a transaction for database consistency
            with transaction.atomic():
                # Track results
                created_count = 0
                updated_count = 0
                skipped_count = 0
                
                # Process each holding
                for zerodha_holding in zerodha_holdings:
                    # Try to find the stock in our database
                    stock = None
                    try:
                        # First try by symbol
                        stock = Stock.objects.get(symbol=zerodha_holding.tradingsymbol)
                    except Stock.DoesNotExist:
                        # Then try by alias
                        try:
                            alias = StockAlias.objects.get(alias=zerodha_holding.tradingsymbol)
                            stock = alias.stock
                        except StockAlias.DoesNotExist:
                            # Create a new stock if not found
                            stock = Stock.objects.create(
                                symbol=zerodha_holding.tradingsymbol,
                                name=zerodha_holding.tradingsymbol,  # Use symbol as name temporarily
                                is_active=True
                            )
                    
                    # If we don't have a stock, skip this holding
                    if not stock:
                        skipped_count += 1
                        continue
                    
                    # Try to find an existing holding for this stock
                    holding, created = Holding.objects.update_or_create(
                        user=user,
                        stock=stock,
                        source="zerodha",
                        defaults={
                            "quantity": zerodha_holding.quantity,
                            "avg_price": zerodha_holding.average_price,
                            "purchase_date": datetime.now().date(),  # We don't get purchase date from Zerodha
                            "external_id": f"{zerodha_holding.tradingsymbol}:{zerodha_holding.exchange}"
                        }
                    )
                    
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1
                
                return {
                    "success": True,
                    "created": created_count,
                    "updated": updated_count,
                    "skipped": skipped_count,
                    "total": len(zerodha_holdings)
                }
                
        except Exception as e:
            logger.error(f"Error syncing Zerodha holdings for user {user_id}: {str(e)}")
            return {"success": False, "message": str(e)}
    
    @staticmethod
    def place_order(
        user_id: int, 
        order_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Place an order on Zerodha.
        
        Args:
            user_id: ID of the user to place order for
            order_data: Order details
            
        Returns:
            Dictionary with order result
        """
        try:
            client = ZerodhaService.get_client_for_user(user_id)
            if not client:
                return {"success": False, "message": "Zerodha client not available"}
            
            # Place the order
            order_id = client.place_order(**order_data)
            
            return {
                "success": True,
                "order_id": order_id,
                "message": "Order placed successfully"
            }
            
        except ZerodhaException as e:
            logger.error(f"Zerodha error placing order for user {user_id}: {str(e)}")
            return {"success": False, "message": str(e)}
        except Exception as e:
            logger.error(f"Error placing Zerodha order for user {user_id}: {str(e)}")
            return {"success": False, "message": f"Internal error: {str(e)}"}
