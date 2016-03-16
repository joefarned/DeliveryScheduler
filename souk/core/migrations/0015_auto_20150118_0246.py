# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_craigpost_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='craigpost',
            name='address',
            field=models.CharField(max_length=450, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='craigpost',
            name='completed',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='craigpost',
            name='price',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
