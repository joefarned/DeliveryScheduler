# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_nest_access_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='nest',
            name='home',
            field=models.CharField(max_length=15, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='nest',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 18, 1, 40, 38, 41162, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
