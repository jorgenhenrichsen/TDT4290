# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-09 08:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resultregistration', '0011_club_competition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='competition',
            field=models.ManyToManyField(blank=True, null=True, to='resultregistration.Competition'),
        ),
    ]
