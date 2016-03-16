# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_request_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='craig',
            field=models.ForeignKey(blank=True, to='core.CraigPost', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='request',
            name='item',
            field=models.ForeignKey(related_name='requests', blank=True, to='core.Item', null=True),
            preserve_default=True,
        ),
    ]
