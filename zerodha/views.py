from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from zerodha.services import ZerodhaService
from zerodha.serializers import (
    ZerodhaHoldingSerializer, ZerodhaOrderSerializer, ZerodhaOrderRequestSerializer
)


class ZerodhaLoginView(APIView):
    """
    API endpoint to get the Zerodha login URL for authentication.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get the Zerodha login URL for the current user.
        """
        login_url = ZerodhaService.get_login_url(request.user.id)
        if login_url:
            return Response({"login_url": login_url}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Zerodha API credentials not configured properly"},
                status=status.HTTP_400_BAD_REQUEST
            )


class ZerodhaCallbackView(APIView):
    """
    API endpoint for handling Zerodha authentication callback.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Handle the Zerodha authentication callback.
        """
        request_token = request.query_params.get('request_token')
        if not request_token:
            return Response(
                {"error": "No request token provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        success = ZerodhaService.generate_session(request.user.id, request_token)
        if success:
            return Response(
                {"success": True, "message": "Zerodha authentication successful"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Failed to authenticate with Zerodha"},
                status=status.HTTP_400_BAD_REQUEST
            )


class ZerodhaHoldingsView(APIView):
    """
    API endpoint to get the user's holdings from Zerodha.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get the current user's holdings from Zerodha.
        """
        client = ZerodhaService.get_client_for_user(request.user.id)
        if not client:
            return Response(
                {"error": "Zerodha API client not available"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            holdings = client.get_holdings()
            serializer = ZerodhaHoldingSerializer(holdings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ZerodhaSyncHoldingsView(APIView):
    """
    API endpoint to sync holdings from Zerodha to the database.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Sync holdings from Zerodha to the database.
        """
        result = ZerodhaService.sync_holdings(request.user.id)
        if result.get("success"):
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)


class ZerodhaOrdersView(APIView):
    """
    API endpoint to get the user's orders from Zerodha.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get the current user's orders from Zerodha.
        """
        client = ZerodhaService.get_client_for_user(request.user.id)
        if not client:
            return Response(
                {"error": "Zerodha API client not available"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            orders = client.get_orders()
            serializer = ZerodhaOrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ZerodhaPlaceOrderView(APIView):
    """
    API endpoint to place an order on Zerodha.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Place an order on Zerodha.
        """
        serializer = ZerodhaOrderRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        result = ZerodhaService.place_order(request.user.id, serializer.validated_data)
        if result.get("success"):
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
