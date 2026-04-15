import os

environment = os.environ.get('DJANGO_ENV', 'dev')

if environment == 'prod':
    from .prod import *
else:
    from .dev import *
