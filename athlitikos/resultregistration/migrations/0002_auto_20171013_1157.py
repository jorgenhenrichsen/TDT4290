# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-13 09:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resultregistration', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Melzer_Faber',
            new_name='MelzerFaber',
        ),
        migrations.AlterField(
            model_name='club',
            name='competition',
            field=models.ManyToManyField(blank=True, to='resultregistration.Competition'),
        ),
    ]
