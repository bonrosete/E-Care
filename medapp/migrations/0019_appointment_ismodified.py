# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-10 11:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medapp', '0018_auto_20170905_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='ismodified',
            field=models.BooleanField(default=0),
        ),
    ]
