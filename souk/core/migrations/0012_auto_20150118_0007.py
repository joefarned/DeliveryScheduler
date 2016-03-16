# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_request_pickup_estimate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='delivery_estimate',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='request',
            name='pickup_estimate',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
