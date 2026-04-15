from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

INSTALLED_APPS += [
    'django_extensions',
]

LOGGING['loggers']['django']['level'] = 'DEBUG'
LOGGING['loggers']['student_management_app']['level'] = 'DEBUG'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
