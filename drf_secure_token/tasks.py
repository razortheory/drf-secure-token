from django.conf import settings
from django.utils import timezone

from celery.task import periodic_task
from celery.schedules import crontab

from drf_secure_token.models import Token


UPDATE_TOKEN = getattr(settings, 'UPDATE_TOKEN', True)


@periodic_task(run_every=crontab(minute=0))
def delete_old_tokens():
    now = timezone.now()

    qs = Token.objects.all()
    if UPDATE_TOKEN:
        qs = qs.filter(dead_in__lt=now)
    else:
        qs = qs.filter(expire_in__lt=now)

    qs.delete()
