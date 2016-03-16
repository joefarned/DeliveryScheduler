# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20150118_0327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='post',
            field=models.ForeignKey(blank=True, to='core.CraigPost', null=True),
            preserve_default=True,
        ),
    ]
