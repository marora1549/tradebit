from rest_framework import serializers
from portfolio.models import Holding, HoldingClass
from core.serializers import StockSerializer, ClassificationSerializer
from users.serializers import UserSerializer


class HoldingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Holding model.
    """
    stock_details = StockSerializer(source='stock', read_only=True)
    user_details = UserSerializer(source='user', read_only=True)
    total_value = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Holding
        fields = [
            'id', 'user', 'stock', 'quantity', 'avg_price',
            'purchase_date', 'notes', 'source', 'external_id',
            'stock_details', 'user_details', 'total_value',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class HoldingClassSerializer(serializers.ModelSerializer):
    """
    Serializer for the HoldingClass model.
    """
    holding_details = HoldingSerializer(source='holding', read_only=True)
    classification_details = ClassificationSerializer(
        source='classification', 
        read_only=True
    )

    class Meta:
        model = HoldingClass
        fields = [
            'id', 'holding', 'classification',
            'holding_details', 'classification_details',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class PortfolioSummarySerializer(serializers.Serializer):
    """
    Serializer for portfolio summary information.
    """
    total_value = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_holdings = serializers.IntegerField()
    sectors = serializers.DictField(child=serializers.DecimalField(max_digits=15, decimal_places=2))
    top_holdings = HoldingSerializer(many=True)
