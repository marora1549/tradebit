from django.urls import path
from users.views import (
    RegisterView, UserProfileView, UserSettingsView, 
    ChangePasswordView, ZerodhaCredentialsView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('settings/', UserSettingsView.as_view(), name='user-settings'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('zerodha-credentials/', ZerodhaCredentialsView.as_view(), name='zerodha-credentials'),
]
