"""Development settings for the tradebit project.

This module contains settings specific to the development environment.
"""

from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Additional development-specific settings
INSTALLED_APPS += [
    'django_extensions',
]

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True

# Disable HTTPS requirements
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
