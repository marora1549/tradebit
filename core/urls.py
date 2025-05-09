from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import StockViewSet, StockAliasViewSet, ClassificationViewSet

router = DefaultRouter()
router.register(r'stocks', StockViewSet)
router.register(r'stock-aliases', StockAliasViewSet)
router.register(r'classifications', ClassificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
