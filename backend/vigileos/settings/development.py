"""
Development settings for VIGILEOSAPP25 project.
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://vigileosapp_dev:dev_password_123@postgres-dev:5432/vigileosapp_dev'
    )
}

# Add development apps
INSTALLED_APPS += [
    # 'django_extensions',  # Commented out for now
]

# Development middleware
MIDDLEWARE += [
    'django.middleware.common.BrokenLinkEmailsMiddleware',
]

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Cache (Redis for development)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': config('REDIS_URL', default='redis://:dev_redis_123@redis-dev:6379/1'),
    }
}

# Static files serving in development
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Development logging
LOGGING['handlers']['console']['level'] = 'DEBUG'
LOGGING['root']['level'] = 'DEBUG'
LOGGING['loggers']['django']['level'] = 'DEBUG'

# Django Debug Toolbar (if installed)
if 'debug_toolbar' in INSTALLED_APPS:
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ['127.0.0.1', '::1']
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
    }

# Development-specific settings
SPECTACULAR_SETTINGS.update({
    'SERVE_INCLUDE_SCHEMA': True,
})

# Disable some security features in development
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False