import uuid
import datetime
from django.conf import settings
from django.db import models
from django.utils import timezone

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
TOKEN_AGE = getattr(settings, 'TOKEN_AGE', 0)

MUTABLE_PERIOD = getattr(settings, 'MUTABLE_PERIOD', 60 * 60 * 24 * 7) # one week by default


class Token(models.Model):
    key = models.CharField(max_length=40, unique=True, null=True, blank=True, default=None)
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='user_auth_tokens')
    created = models.DateTimeField(auto_now_add=True)
    expire_in = models.DateTimeField(default=datetime.datetime.now)
    dead_in = models.DateTimeField(default=datetime.datetime.now)

    marked_for_delete = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.key = Token.generate_key()
            self.expire_in = timezone.now() + datetime.timedelta(seconds=TOKEN_AGE)
            self.dead_in = self.expire_in + datetime.timedelta(seconds=MUTABLE_PERIOD)
        return super(Token, self).save(*args, **kwargs)

    @staticmethod
    def generate_key():
        return str(uuid.uuid4())

    def __unicode__(self):
        return self.key
