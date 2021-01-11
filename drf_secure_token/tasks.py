from django.utils import timezone

from celery import VERSION as CELERY_VERSION
from celery.schedules import crontab

from drf_secure_token.models import Token
from drf_secure_token.settings import settings as token_settings


def delete_old_tokens():
    now = timezone.now()

    qs = Token.objects.all()
    qs = qs.filter(dead_in__lt=now)

    qs.delete()


# if setting enabled and default app exists (celery<5), use it. else just register task to be available for scheduler
if CELERY_VERSION < (5, 0, 0):
    if token_settings.REMOVE_TOKENS_THROUGH_CELERY:
        from celery.task import periodic_task
        delete_old_tokens = periodic_task(run_every=crontab(minute=0))(delete_old_tokens)
    else:
        from celery.task import task
        delete_old_tokens = task(delete_old_tokens)
else:
    from celery import shared_task
    delete_old_tokens = shared_task(delete_old_tokens)

    DELETE_OLD_TOKENS = {
        'task': 'drf_secure_token.tasks.delete_old_tokens',
        'schedule': crontab(minute=0),
        'args': ()
    }
