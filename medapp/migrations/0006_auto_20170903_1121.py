# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-03 03:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medapp', '0005_auto_20170903_1055'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medicalhistory',
            old_name='status',
            new_name='date',
        ),
    ]
