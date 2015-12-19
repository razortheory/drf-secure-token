# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drf_secure_token', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=None, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='token',
            name='key',
            field=models.CharField(unique=True, max_length=40),
            preserve_default=True,
        ),
    ]
