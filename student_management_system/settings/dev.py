import os
from dotenv import load_dotenv
from .base import *

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-insecure')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
