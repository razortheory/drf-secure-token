import os
import uuid
from django.conf import settings
from django.db import models


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Token(models.Model):
    key = models.CharField(max_length=40, unique=True)
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='user_auth_tokens')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        return str(uuid.uuid4())

    def update_key(self):
        generated_key = self.generate_key()
        self.update(key=generated_key)
        return generated_key

    def __unicode__(self):
        return self.key
