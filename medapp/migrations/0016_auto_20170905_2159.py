# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-05 21:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medapp', '0015_loginrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginrecord',
            name='username',
            field=models.CharField(max_length=20),
        ),
    ]
