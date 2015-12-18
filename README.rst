================
DRF Secure Token
================

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'rest_framework',
        'drf_secure_token',
    ]

2. Add following lines to your settings.py:

    REST_FRAMEWORK = {
        ...
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.BasicAuthentication',
            'drf_secure_token.authentication.SecureTokenAuthentication',
            ...
         ),
        ...
    }

3. Run `python manage.py migrate` to create the drf_secure_token models.
