from django.urls import path, include
from rest_framework.routers import DefaultRouter
from portfolio.views import HoldingViewSet, HoldingClassViewSet, PortfolioSummaryView

router = DefaultRouter()
router.register(r'holdings', HoldingViewSet, basename='holding')
router.register(r'holding-classes', HoldingClassViewSet, basename='holdingclass')

urlpatterns = [
    path('', include(router.urls)),
    path('summary/', PortfolioSummaryView.as_view(), name='portfolio-summary'),
]
