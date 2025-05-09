from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import UserSettings

User = get_user_model()


class UserModelTest(TestCase):
    """
    Test suite for the User model.
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

    def test_user_creation(self):
        self.assertEqual(self.user.username, self.user_data['username'])
        self.assertEqual(self.user.email, self.user_data['email'])
        self.assertEqual(self.user.first_name, self.user_data['first_name'])
        self.assertEqual(self.user.last_name, self.user_data['last_name'])
        self.assertEqual(self.user.bio, self.user_data['bio'])
        self.assertTrue(self.user.check_password(self.user_data['password']))

    def test_user_str_representation(self):
        self.assertEqual(str(self.user), self.user_data['username'])

    def test_user_settings_auto_creation(self):
        # Verify that UserSettings was automatically created for the user
        settings = UserSettings.objects.filter(user=self.user).first()
        self.assertIsNotNone(settings)
        self.assertEqual(settings.theme, 'system')
        self.assertEqual(settings.default_view, 'portfolio')


class UserSettingsModelTest(TestCase):
    """
    Test suite for the UserSettings model.
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
            default_view='watchlist',
            zerodha_api_key='test_api_key',
            zerodha_api_secret='test_api_secret',
            notifications_enabled=True,
            email_notifications=False
        )

    def test_user_settings_creation(self):
        self.assertEqual(self.user_settings.user, self.user)
        self.assertEqual(self.user_settings.theme, 'dark')
        self.assertEqual(self.user_settings.default_view, 'watchlist')
        self.assertEqual(self.user_settings.zerodha_api_key, 'test_api_key')
        self.assertEqual(self.user_settings.zerodha_api_secret, 'test_api_secret')
        self.assertTrue(self.user_settings.notifications_enabled)
        self.assertFalse(self.user_settings.email_notifications)

    def test_user_settings_str_representation(self):
        self.assertEqual(str(self.user_settings), "testuser's Settings")
