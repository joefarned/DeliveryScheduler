# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_request_cost_delivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='delivery_estimate',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 18, 5, 2, 47, 844672, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='request',
            name='delivery_id',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
    ]
