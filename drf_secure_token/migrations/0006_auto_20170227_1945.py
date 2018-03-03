# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('drf_secure_token', '0005_auto_20170227_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='expire_in',
            field=models.DateTimeField(default=timezone.now),
        ),
        migrations.AlterField(
            model_name='token',
            name='dead_in',
            field=models.DateTimeField(default=timezone.now),
        ),
    ]
