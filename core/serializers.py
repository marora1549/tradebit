from rest_framework import serializers
from core.models import Stock, StockAlias, Classification


class StockSerializer(serializers.ModelSerializer):
    """
    Serializer for the Stock model.
    """
    class Meta:
        model = Stock
        fields = ['id', 'symbol', 'name', 'sector', 'industry', 'is_active']


class StockAliasSerializer(serializers.ModelSerializer):
    """
    Serializer for the StockAlias model.
    """
    stock_details = StockSerializer(source='stock', read_only=True)

    class Meta:
        model = StockAlias
        fields = ['id', 'stock', 'alias', 'stock_details']


class ClassificationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Classification model.
    """
    class Meta:
        model = Classification
        fields = ['id', 'name', 'type', 'description']
