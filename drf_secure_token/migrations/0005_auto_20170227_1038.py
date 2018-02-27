# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('drf_secure_token', '0004_auto_20160422_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='user',
            field=models.ForeignKey(related_name='user_auth_tokens', to=settings.AUTH_USER_MODEL, on_delete=models.deletion.CASCADE),
        ),
    ]
