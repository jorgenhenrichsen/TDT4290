# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-04 21:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resultregistration', '0006_auto_20171104_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='lifter_club',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resultregistration.Club'),
        ),
    ]
