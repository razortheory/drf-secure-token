import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = 'secret-key'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',

    'drf_secure_token',
    'tests',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}
