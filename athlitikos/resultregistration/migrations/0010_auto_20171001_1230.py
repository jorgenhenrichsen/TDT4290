# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-01 12:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resultregistration', '0009_auto_20170926_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='clubName',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='club',
            name='region',
            field=models.CharField(max_length=100),
        ),
    ]
