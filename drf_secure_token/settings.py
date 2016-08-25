from django.conf import settings


TOKEN_AGE = getattr(settings, 'TOKEN_AGE', 0)
UPDATE_TOKEN = getattr(settings, 'UPDATE_TOKEN', not settings.DEBUG)


MUTABLE_PERIOD = getattr(settings, 'MUTABLE_PERIOD', 60 * 60 * 24 * 7)  # One week by default


REMOVE_TOKENS_THROUGH_CELERY = getattr(settings, 'REMOVE_TOKENS_THROUGH_CELERY', False)


DEFAULT_TOKEN_CHECKERS = [
    'drf_secure_token.checkers.ActiveUserChecker',
]
if TOKEN_AGE:
    if UPDATE_TOKEN:
        DEFAULT_TOKEN_CHECKERS.append('drf_secure_token.checkers.DeadTokenChecker')
    else:
        DEFAULT_TOKEN_CHECKERS.append('drf_secure_token.checkers.ExpireTokenChecker')


TOKEN_CHECKERS = getattr(settings, 'TOKEN_CHECKERS', DEFAULT_TOKEN_CHECKERS)
