"""
Django development settings for student_management_system.
"""

from .base import *


DEBUG = True


ALLOWED_HOSTS = ["*"]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


LOGGING["loggers"]["django"]["level"] = "DEBUG"
LOGGING["loggers"]["student_management_app"]["level"] = "DEBUG"


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]


MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
