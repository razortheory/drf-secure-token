================
DRF Secure Token
================

Quick start
-----------

1. Add "drf_secure_token" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'rest_framework',
        'drf_secure_token',
    ]

2. Add following lines to your settings.py::

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.BasicAuthentication',
            'drf_secure_token.authentication.SecureTokenAuthentication',
         ]
    }

3. For updating token add this middleware to your MIDDLEWARE_CLASSES::

    MIDDLEWARE_CLASSES = (
        ...
        'drf_secure_token.middleware.UpdateTokenMiddleware',
    )

4. Add TOKEN_AGE to your settings::

    TOKEN_AGE = 60*10 # 10 min

4. Run `python manage.py migrate` to create the drf_secure_token models.
