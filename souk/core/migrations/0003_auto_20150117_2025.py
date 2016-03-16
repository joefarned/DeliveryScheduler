# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import souk.core.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_auto_20150117_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=250)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Nest',
                'verbose_name_plural': 'Nests',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='item',
            name='picture',
            field=models.ImageField(upload_to=souk.core.models.get_file_path, blank=True),
            preserve_default=True,
        ),
    ]
