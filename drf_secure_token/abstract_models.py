import datetime
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

from rest_framework import exceptions

from drf_secure_token import checkers
from drf_secure_token.settings import settings as token_settings


class BaseToken(models.Model):
    @staticmethod
    def generate_key():
        return str(uuid.uuid4())

    key = models.CharField(max_length=40, unique=True, blank=True, default=generate_key.__func__)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_auth_tokens', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.key

    def check_token(self):
        for checker in checkers.checkers:
            if not checker.check(self):
                raise exceptions.AuthenticationFailed(checker.error_message)


class ExpiredTokenMixin(models.Model):
    @staticmethod
    def default_expire_time():
        return timezone.now() + datetime.timedelta(seconds=token_settings.TOKEN_AGE)

    expire_in = models.DateTimeField(default=default_expire_time.__func__)

    class Meta:
        abstract = True


class DyingTokenMixin(ExpiredTokenMixin):
    @staticmethod
    def default_dead_time():
        return ExpiredTokenMixin.default_expire_time() + datetime.timedelta(seconds=token_settings.MUTABLE_PERIOD)

    dead_in = models.DateTimeField(default=default_dead_time.__func__)
    marked_for_delete = models.BooleanField(default=False)

    class Meta:
        abstract = True
