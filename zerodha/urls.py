from django.urls import path
from zerodha.views import (
    ZerodhaLoginView, ZerodhaCallbackView, ZerodhaHoldingsView, 
    ZerodhaSyncHoldingsView, ZerodhaOrdersView, ZerodhaPlaceOrderView
)

urlpatterns = [
    # Authentication
    path('login/', ZerodhaLoginView.as_view(), name='zerodha-login'),
    path('callback/', ZerodhaCallbackView.as_view(), name='zerodha-callback'),
    
    # Holdings
    path('holdings/', ZerodhaHoldingsView.as_view(), name='zerodha-holdings'),
    path('sync-holdings/', ZerodhaSyncHoldingsView.as_view(), name='zerodha-sync-holdings'),
    
    # Orders
    path('orders/', ZerodhaOrdersView.as_view(), name='zerodha-orders'),
    path('place-order/', ZerodhaPlaceOrderView.as_view(), name='zerodha-place-order'),
]
