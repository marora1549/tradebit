from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField
from django.db.models.functions import Coalesce
from rest_framework import viewsets, filters, views, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from portfolio.models import Holding, HoldingClass
from portfolio.serializers import (
    HoldingSerializer, HoldingClassSerializer, PortfolioSummarySerializer
)


class HoldingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows holdings to be viewed or edited.
    """
    serializer_class = HoldingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'stock', 'source']
    search_fields = ['stock__symbol', 'stock__name', 'notes']
    ordering_fields = ['purchase_date', 'quantity', 'avg_price']

    def get_queryset(self):
        """
        This view should return a list of all holdings for the currently authenticated user.
        """
        return Holding.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Set the user to the current user if not provided.
        """
        if not serializer.validated_data.get('user'):
            serializer.save(user=self.request.user)
        else:
            serializer.save()


class HoldingClassViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows holding classifications to be viewed or edited.
    """
    serializer_class = HoldingClassSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['holding', 'classification']

    def get_queryset(self):
        """
        This view should return a list of all holding classifications for holdings
        owned by the currently authenticated user.
        """
        return HoldingClass.objects.filter(holding__user=self.request.user)


class PortfolioSummaryView(views.APIView):
    """
    API endpoint that provides a summary of the user's portfolio.
    """
    def get(self, request, format=None):
        """
        Return a summary of the user's portfolio.
        """
        user = request.user
        
        # Calculate total portfolio value
        holdings = Holding.objects.filter(user=user)
        value_expr = ExpressionWrapper(
            F('quantity') * F('avg_price'), 
            output_field=DecimalField()
        )
        
        holdings = holdings.annotate(value=value_expr)
        total_value = holdings.aggregate(total=Coalesce(Sum('value'), 0))['total']
        total_holdings = holdings.count()
        
        # Group by sector
        sector_values = {}
        sector_groups = holdings.values('stock__sector').annotate(
            sector_value=Sum('value')
        )
        
        for group in sector_groups:
            sector = group['stock__sector'] or 'Unknown'
            sector_values[sector] = group['sector_value']
        
        # Get top holdings by value
        top_holdings = holdings.order_by('-value')[:5]
        
        # Create response data
        response_data = {
            'total_value': total_value,
            'total_holdings': total_holdings,
            'sectors': sector_values,
            'top_holdings': top_holdings
        }
        
        serializer = PortfolioSummarySerializer(response_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
