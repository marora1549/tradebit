from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from users.models import UserSettings

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_image']
        read_only_fields = ['id']


class UserSettingsSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserSettings model.
    """
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = UserSettings
        fields = [
            'id', 'user', 'theme', 'default_view',
            'zerodha_api_key', 'zerodha_api_secret',
            'notifications_enabled', 'email_notifications',
            'user_details'
        ]
        read_only_fields = ['id', 'user', 'zerodha_api_key', 'zerodha_api_secret']
        extra_kwargs = {
            'zerodha_api_key': {'write_only': True},
            'zerodha_api_secret': {'write_only': True},
        }


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        
        # Create default user settings
        UserSettings.objects.create(user=user)
        
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs


class ZerodhaCredentialsSerializer(serializers.Serializer):
    """
    Serializer for updating Zerodha API credentials.
    """
    api_key = serializers.CharField(required=True)
    api_secret = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        instance.zerodha_api_key = validated_data.get('api_key', instance.zerodha_api_key)
        instance.zerodha_api_secret = validated_data.get('api_secret', instance.zerodha_api_secret)
        instance.save()
        return instance
