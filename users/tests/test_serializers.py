from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import UserSettings
from users.serializers import (
    UserSerializer, UserSettingsSerializer, RegisterSerializer, ChangePasswordSerializer
)

User = get_user_model()


class UserSerializerTest(TestCase):
    """
    Test suite for the UserSerializer.
    """
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'bio': 'This is a test user.'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.serializer = UserSerializer(instance=self.user)

    def test_user_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            set(['id', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_image'])
        )

    def test_user_serializer_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['username'], self.user_data['username'])
        self.assertEqual(data['email'], self.user_data['email'])
        self.assertEqual(data['first_name'], self.user_data['first_name'])
        self.assertEqual(data['last_name'], self.user_data['last_name'])
        self.assertEqual(data['bio'], self.user_data['bio'])


class UserSettingsSerializerTest(TestCase):
    """
    Test suite for the UserSettingsSerializer.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user_settings = UserSettings.objects.create(
            user=self.user,
            theme='dark',
            default_view='analytics',
            zerodha_api_key='test_api_key',
            zerodha_api_secret='test_api_secret'
        )
        self.serializer = UserSettingsSerializer(instance=self.user_settings)

    def test_user_settings_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            set([
                'id', 'user', 'theme', 'default_view',
                'notifications_enabled', 'email_notifications',
                'user_details'
            ])
        )
        # Verify that sensitive fields are not included
        self.assertNotIn('zerodha_api_key', data)
        self.assertNotIn('zerodha_api_secret', data)

    def test_user_settings_serializer_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['user'], self.user.id)
        self.assertEqual(data['theme'], 'dark')
        self.assertEqual(data['default_view'], 'analytics')
        self.assertTrue(data['notifications_enabled'])
        self.assertTrue(data['email_notifications'])


class RegisterSerializerTest(TestCase):
    """
    Test suite for the RegisterSerializer.
    """
    def setUp(self):
        self.valid_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'Password123!',
            'password2': 'Password123!',
            'first_name': 'New',
            'last_name': 'User'
        }
        self.serializer = RegisterSerializer(data=self.valid_data)

    def test_register_serializer_validation(self):
        self.assertTrue(self.serializer.is_valid())

    def test_register_serializer_password_mismatch(self):
        invalid_data = self.valid_data.copy()
        invalid_data['password2'] = 'DifferentPassword123!'
        serializer = RegisterSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_register_serializer_create_user(self):
        self.serializer.is_valid()
        user = self.serializer.save()
        self.assertEqual(user.username, self.valid_data['username'])
        self.assertEqual(user.email, self.valid_data['email'])
        self.assertEqual(user.first_name, self.valid_data['first_name'])
        self.assertEqual(user.last_name, self.valid_data['last_name'])
        self.assertTrue(user.check_password(self.valid_data['password']))

        # Check that UserSettings was created for the new user
        self.assertTrue(hasattr(user, 'settings'))


class ChangePasswordSerializerTest(TestCase):
    """
    Test suite for the ChangePasswordSerializer.
    """
    def setUp(self):
        self.valid_data = {
            'old_password': 'OldPassword123!',
            'new_password': 'NewPassword123!',
            'new_password2': 'NewPassword123!'
        }
        self.serializer = ChangePasswordSerializer(data=self.valid_data)

    def test_change_password_serializer_validation(self):
        self.assertTrue(self.serializer.is_valid())

    def test_change_password_serializer_password_mismatch(self):
        invalid_data = self.valid_data.copy()
        invalid_data['new_password2'] = 'DifferentPassword123!'
        serializer = ChangePasswordSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('new_password', serializer.errors)
