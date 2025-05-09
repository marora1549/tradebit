from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel


class User(AbstractUser, TimeStampedModel):
    """
    Custom user model that extends Django's built-in User model.
    """
    email = models.EmailField(_('Email Address'), unique=True)
    bio = models.TextField(_('Biography'), blank=True, null=True)
    profile_image = models.ImageField(
        _('Profile Image'),
        upload_to='profile_images/',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username


class UserSettings(TimeStampedModel):
    """
    Model for storing user-specific settings and preferences.
    """
    THEME_CHOICES = [
        ('light', _('Light')),
        ('dark', _('Dark')),
        ('system', _('System Default')),
    ]
    
    DEFAULT_VIEW_CHOICES = [
        ('portfolio', _('Portfolio')),
        ('watchlist', _('Watchlist')),
        ('analytics', _('Analytics')),
    ]
    
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name='settings',
        verbose_name=_('User')
    )
    theme = models.CharField(
        _('Theme'),
        max_length=20,
        choices=THEME_CHOICES,
        default='system'
    )
    default_view = models.CharField(
        _('Default View'),
        max_length=20,
        choices=DEFAULT_VIEW_CHOICES,
        default='portfolio'
    )
    zerodha_api_key = models.CharField(
        _('Zerodha API Key'),
        max_length=100,
        blank=True,
        null=True
    )
    zerodha_api_secret = models.CharField(
        _('Zerodha API Secret'),
        max_length=100,
        blank=True,
        null=True
    )
    zerodha_request_token = models.CharField(
        _('Zerodha Request Token'),
        max_length=100,
        blank=True,
        null=True
    )
    zerodha_access_token = models.CharField(
        _('Zerodha Access Token'),
        max_length=100,
        blank=True,
        null=True
    )
    zerodha_refresh_token = models.CharField(
        _('Zerodha Refresh Token'),
        max_length=100,
        blank=True,
        null=True
    )
    zerodha_session_expiry = models.DateTimeField(
        _('Zerodha Session Expiry'),
        blank=True,
        null=True
    )
    notifications_enabled = models.BooleanField(
        _('Notifications Enabled'),
        default=True
    )
    email_notifications = models.BooleanField(
        _('Email Notifications'),
        default=True
    )

    class Meta:
        verbose_name = _('User Settings')
        verbose_name_plural = _('User Settings')

    def __str__(self):
        return f"{self.user.username}'s Settings"
