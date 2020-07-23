# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drf_secure_token', '0002_token_expire_in'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='key',
            field=models.CharField(default=None, max_length=40, unique=True, null=True, blank=True),
        ),
    ]
