# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20150118_0246'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='craig',
            field=models.ForeignKey(default=-1, blank=True, to='core.CraigPost'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='request',
            name='item',
            field=models.ForeignKey(related_name='requests', blank=True, to='core.Item'),
            preserve_default=True,
        ),
    ]
