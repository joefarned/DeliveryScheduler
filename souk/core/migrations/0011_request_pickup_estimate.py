# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20150118_0002'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='pickup_estimate',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 18, 5, 5, 51, 828643, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
    ]
