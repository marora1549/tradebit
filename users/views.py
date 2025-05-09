from django.contrib.auth import get_user_model
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import UserSettings
from users.serializers import (
    UserSerializer, UserSettingsSerializer, RegisterSerializer, 
    ChangePasswordSerializer, ZerodhaCredentialsSerializer
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    """
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating the user profile.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserSettingsView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating user settings.
    """
    serializer_class = UserSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return UserSettings.objects.get_or_create(user=self.request.user)[0]


class ChangePasswordView(APIView):
    """
    API endpoint for changing the user password.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            
            # Check if old password is correct
            if not user.check_password(old_password):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Set the new password
            user.set_password(new_password)
            user.save()
            return Response(
                {"message": "Password updated successfully."},
                status=status.HTTP_200_OK
            )
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ZerodhaCredentialsView(APIView):
    """
    API endpoint for updating Zerodha API credentials.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_settings = UserSettings.objects.get_or_create(user=request.user)[0]
        serializer = ZerodhaCredentialsSerializer(data=request.data)
        
        if serializer.is_valid():
            # Update the credentials
            user_settings.zerodha_api_key = serializer.validated_data['api_key']
            user_settings.zerodha_api_secret = serializer.validated_data['api_secret']
            user_settings.save()
            
            return Response(
                {"message": "Zerodha credentials updated successfully."},
                status=status.HTTP_200_OK
            )
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
