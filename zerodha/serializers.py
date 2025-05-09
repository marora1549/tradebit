from rest_framework import serializers
from typing import Dict, List, Any


class ZerodhaHoldingSerializer(serializers.Serializer):
    """
    Serializer for Zerodha holdings data.
    """
    tradingsymbol = serializers.CharField()
    exchange = serializers.CharField()
    isin = serializers.CharField(allow_null=True)
    quantity = serializers.FloatField()
    average_price = serializers.FloatField()
    last_price = serializers.FloatField()
    pnl = serializers.FloatField()
    day_change = serializers.FloatField(required=False, default=0.0)
    day_change_percentage = serializers.FloatField(required=False, default=0.0)
    product = serializers.CharField()


class ZerodhaOrderSerializer(serializers.Serializer):
    """
    Serializer for Zerodha order data.
    """
    order_id = serializers.CharField()
    exchange = serializers.CharField()
    tradingsymbol = serializers.CharField()
    transaction_type = serializers.CharField()
    order_type = serializers.CharField()
    quantity = serializers.FloatField()
    price = serializers.FloatField(allow_null=True)
    status = serializers.CharField()
    filled_quantity = serializers.FloatField(default=0.0)
    pending_quantity = serializers.FloatField(default=0.0)
    average_price = serializers.FloatField(allow_null=True)


class ZerodhaOrderRequestSerializer(serializers.Serializer):
    """
    Serializer for Zerodha order request data.
    """
    exchange = serializers.CharField()
    tradingsymbol = serializers.CharField()
    transaction_type = serializers.CharField()  # BUY or SELL
    quantity = serializers.FloatField()
    product = serializers.CharField()  # CNC, MIS, etc.
    order_type = serializers.CharField()  # MARKET, LIMIT, etc.
    price = serializers.FloatField(required=False, allow_null=True)
    trigger_price = serializers.FloatField(required=False, allow_null=True)
    validity = serializers.CharField(required=False, default="DAY")
    disclosed_quantity = serializers.FloatField(required=False, default=0.0)
    squareoff = serializers.FloatField(required=False, allow_null=True)
    stoploss = serializers.FloatField(required=False, allow_null=True)
    trailing_stoploss = serializers.FloatField(required=False, allow_null=True)
    tag = serializers.CharField(required=False, allow_null=True)


class ZerodhaProfileSerializer(serializers.Serializer):
    """
    Serializer for Zerodha user profile data.
    """
    user_id = serializers.CharField()
    user_name = serializers.CharField()
    user_shortname = serializers.CharField()
    email = serializers.EmailField()
    user_type = serializers.CharField()
    broker = serializers.CharField()
