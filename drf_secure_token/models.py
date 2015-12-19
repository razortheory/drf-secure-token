import os
import uuid
import datetime
from django.conf import settings
from django.db import models


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
TOKEN_AGE = getattr(settings, 'TOKEN_AGE', 0)


class Token(models.Model):
    key = models.CharField(max_length=40, unique=True)
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='user_auth_tokens')
    created = models.DateTimeField(auto_now_add=True)
    expire_in = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.key = Token.generate_key()
            self.expire_in = datetime.datetime.now() + datetime.timedelta(seconds=TOKEN_AGE)
        return super(Token, self).save(*args, **kwargs)

    @staticmethod
    def generate_key():
        return str(uuid.uuid4())

    def __unicode__(self):
        return self.key
