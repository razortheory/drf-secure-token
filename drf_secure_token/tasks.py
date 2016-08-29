from django.utils import timezone

from celery.task import periodic_task
from celery.schedules import crontab

from drf_secure_token.models import Token
from drf_secure_token.settings import REMOVE_TOKENS_THROUGH_CELERY


if REMOVE_TOKENS_THROUGH_CELERY:
    @periodic_task(run_every=crontab(minute=0))
    def delete_old_tokens():
        now = timezone.now()

        qs = Token.objects.all()
        qs = qs.filter(dead_in__lt=now)

        qs.delete()
