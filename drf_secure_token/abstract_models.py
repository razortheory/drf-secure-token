import datetime
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.six import python_2_unicode_compatible
from rest_framework import exceptions

from drf_secure_token import checkers
from drf_secure_token.settings import settings as token_settings


@python_2_unicode_compatible
class BaseToken(models.Model):
    key = models.CharField(max_length=40, unique=True, null=True, blank=True, default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_auth_tokens', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.key

    @staticmethod
    def generate_key():
        return str(uuid.uuid4())

    def save(self, *args, **kwargs):
        if not self.pk:
            self.key = self.generate_key()
        return super(BaseToken, self).save(*args, **kwargs)

    def check_token(self):
        for checker in checkers.checkers:
            if not checker.check(self):
                raise exceptions.AuthenticationFailed(checker.error_message)


class ExpiredTokenMixin(models.Model):
    expire_in = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expire_in = timezone.now() + datetime.timedelta(seconds=token_settings.TOKEN_AGE)
        super(ExpiredTokenMixin, self).save(*args, **kwargs)


class DyingTokenMixin(ExpiredTokenMixin):
    dead_in = models.DateTimeField(default=timezone.now)
    marked_for_delete = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expire_in = timezone.now() + datetime.timedelta(seconds=token_settings.TOKEN_AGE)
            self.dead_in = self.expire_in + datetime.timedelta(seconds=token_settings.MUTABLE_PERIOD)
        return super(ExpiredTokenMixin, self).save(*args, **kwargs)
