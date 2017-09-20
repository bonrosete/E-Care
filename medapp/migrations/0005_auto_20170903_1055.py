# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-03 02:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medapp', '0004_auto_20170902_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='endtime',
            field=models.CharField(default='12:00am', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointment',
            name='starttime',
            field=models.CharField(default='12:30am', max_length=10),
            preserve_default=False,
        ),
    ]
