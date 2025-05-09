from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import UserSettings

User = get_user_model()


class RegistrationViewTest(APITestCase):
    """
    Test suite for the RegisterView API endpoint.
    """
    def setUp(self):
        self.register_url = reverse('register')
        self.valid_payload = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'first_name': 'New',
            'last_name': 'User'
        }

    def test_registration_success(self):
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'newuser')
        
        # Verify user settings were created
        self.assertEqual(UserSettings.objects.count(), 1)

    def test_registration_password_mismatch(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload['password2'] = 'DifferentPassword123!'
        response = self.client.post(self.register_url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_registration_duplicate_username(self):
        # Create a user first
        User.objects.create_user(
            username='newuser',
            email='existing@example.com',
            password='test123'
        )
        
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)


class UserProfileViewTest(APITestCase):
    """
    Test suite for the UserProfileView API endpoint.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            bio='Test bio'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.profile_url = reverse('profile')

    def test_get_profile(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['bio'], 'Test bio')

    def test_update_profile(self):
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'bio': 'Updated bio'
        }
        response = self.client.patch(self.profile_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh the user from the database
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')
        self.assertEqual(self.user.bio, 'Updated bio')

    def test_unauthorized_access(self):
        self.client.logout()
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserSettingsViewTest(APITestCase):
    """
    Test suite for the UserSettingsView API endpoint.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user_settings = UserSettings.objects.create(
            user=self.user,
            theme='system',
            default_view='portfolio'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.settings_url = reverse('user-settings')

    def test_get_settings(self):
        response = self.client.get(self.settings_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['theme'], 'system')
        self.assertEqual(response.data['default_view'], 'portfolio')

    def test_update_settings(self):
        update_data = {
            'theme': 'dark',
            'default_view': 'analytics',
            'notifications_enabled': False,
            'email_notifications': False
        }
        response = self.client.patch(self.settings_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh the settings from the database
        self.user_settings.refresh_from_db()
        self.assertEqual(self.user_settings.theme, 'dark')
        self.assertEqual(self.user_settings.default_view, 'analytics')
        self.assertFalse(self.user_settings.notifications_enabled)
        self.assertFalse(self.user_settings.email_notifications)

    def test_unauthorized_access(self):
        self.client.logout()
        response = self.client.get(self.settings_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ChangePasswordViewTest(APITestCase):
    """
    Test suite for the ChangePasswordView API endpoint.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='OldPassword123!'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.change_password_url = reverse('change-password')
        self.valid_payload = {
            'old_password': 'OldPassword123!',
            'new_password': 'NewPassword123!',
            'new_password2': 'NewPassword123!'
        }

    def test_change_password_success(self):
        response = self.client.post(
            self.change_password_url, 
            self.valid_payload, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the password was changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPassword123!'))

    def test_change_password_incorrect_old_password(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload['old_password'] = 'WrongPassword123!'
        response = self.client.post(
            self.change_password_url, 
            invalid_payload, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verify the password was not changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('OldPassword123!'))

    def test_change_password_mismatch(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload['new_password2'] = 'DifferentPassword123!'
        response = self.client.post(
            self.change_password_url, 
            invalid_payload, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verify the password was not changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('OldPassword123!'))

    def test_unauthorized_access(self):
        self.client.logout()
        response = self.client.post(
            self.change_password_url, 
            self.valid_payload, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
