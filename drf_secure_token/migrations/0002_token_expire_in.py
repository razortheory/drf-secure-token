# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('drf_secure_token', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='expire_in',
            field=models.DateTimeField(default=timezone.now),
            preserve_default=True,
        ),
    ]
