# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 07:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resultregistration', '0005_auto_20171024_1655'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='age',
        ),
    ]
