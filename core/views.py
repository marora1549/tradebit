from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Stock, StockAlias, Classification
from core.serializers import StockSerializer, StockAliasSerializer, ClassificationSerializer


class StockViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows stocks to be viewed or edited.
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sector', 'industry', 'is_active']
    search_fields = ['symbol', 'name']
    ordering_fields = ['symbol', 'name', 'sector', 'industry']


class StockAliasViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows stock aliases to be viewed or edited.
    """
    queryset = StockAlias.objects.all()
    serializer_class = StockAliasSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['stock']
    search_fields = ['alias', 'stock__symbol', 'stock__name']


class ClassificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows classifications to be viewed or edited.
    """
    queryset = Classification.objects.all()
    serializer_class = ClassificationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type']
    search_fields = ['name', 'type', 'description']
    ordering_fields = ['name', 'type']
