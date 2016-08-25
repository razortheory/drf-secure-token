import uuid
import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from rest_framework import exceptions

from drf_secure_token.checkers import checkers
from drf_secure_token.settings import TOKEN_AGE, MUTABLE_PERIOD


class BaseToken(models.Model):
    key = models.CharField(max_length=40, unique=True, null=True, blank=True, default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_auth_tokens')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.key

    @staticmethod
    def generate_key():
        return str(uuid.uuid4())

    def save(self, *args, **kwargs):
        if not self.pk:
            self.key = self.generate_key()
        return super(BaseToken, self).save(*args, **kwargs)

    def check_token(self):
        for checker in checkers:
            if not checker.check(self):
                raise exceptions.AuthenticationFailed(checker.error_message)


class ExpiredTokenMixin(models.Model):
    expire_in = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expire_in = timezone.now() + datetime.timedelta(seconds=TOKEN_AGE)
        super(ExpiredTokenMixin, self).save(*args, **kwargs)


class DyingTokenMixin(ExpiredTokenMixin):
    dead_in = models.DateTimeField(default=datetime.datetime.now)
    marked_for_delete = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expire_in = timezone.now() + datetime.timedelta(seconds=TOKEN_AGE)
            self.dead_in = self.expire_in + datetime.timedelta(seconds=MUTABLE_PERIOD)
        return super(ExpiredTokenMixin, self).save(*args, **kwargs)


class Token(DyingTokenMixin, BaseToken):
    class Meta:
        verbose_name = _('Token')
        verbose_name_plural = _('Tokens')
