# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20150118_0007'),
    ]

    operations = [
        migrations.CreateModel(
            name='CraigPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('title', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=75)),
                ('added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'CraigPost',
                'verbose_name_plural': 'CraigPosts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('from_us', models.BooleanField(default=True)),
                ('post', models.ForeignKey(to='core.CraigPost')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='request',
            name='item',
            field=models.ForeignKey(related_name='requests', to='core.Item'),
            preserve_default=True,
        ),
    ]
