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

4. Add UPDATE_TOKEN to your 'dev' settings if you don't want to update token in DEBUG mode::

    UPDATE_TOKEN = False

5. Add TOKEN_AGE to your settings::

    TOKEN_AGE = 60*10 # 10 min

6. (Optional) To cleanup dead tokens celery can be used. Way to enable depends from celery version

6.1 Celery 4, just enable it with settings::

    REMOVE_TOKENS_THROUGH_CELERY = True

6.2 Celery 5, add periodic task manually::

    @app.on_after_finalize.connect
    def setup_periodic_tasks(sender, **kwargs):
        from drf_secure_token.tasks import DELETE_OLD_TOKENS

        app.conf.beat_schedule.update({
            'drf_secure_token.tasks.delete_old_tokens': DELETE_OLD_TOKENS,
        })

7. Run `python manage.py migrate` to create the drf_secure_token models.
