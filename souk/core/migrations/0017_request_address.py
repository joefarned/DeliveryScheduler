# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20150118_0322'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='address',
            field=models.CharField(max_length=450, blank=True),
            preserve_default=True,
        ),
    ]
