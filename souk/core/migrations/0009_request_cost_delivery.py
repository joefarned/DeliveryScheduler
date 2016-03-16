# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20150117_2248'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='cost_delivery',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
