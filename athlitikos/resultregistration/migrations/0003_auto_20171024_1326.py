# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-24 11:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resultregistration', '0002_pentathlonresult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pentathlonresult',
            name='forty_meter',
            field=models.DecimalField(decimal_places=10, max_digits=10),
        ),
        migrations.AlterField(
            model_name='pentathlonresult',
            name='forty_meter_points',
            field=models.DecimalField(decimal_places=10, max_digits=10),
        ),
        migrations.AlterField(
            model_name='pentathlonresult',
            name='jump',
            field=models.DecimalField(decimal_places=10, max_digits=10),
        ),
        migrations.AlterField(
            model_name='pentathlonresult',
            name='jump_points',
            field=models.DecimalField(decimal_places=10, max_digits=10),
        ),
        migrations.AlterField(
            model_name='pentathlonresult',
            name='shot_put',
            field=models.DecimalField(decimal_places=10, max_digits=10),
        ),
        migrations.AlterField(
            model_name='pentathlonresult',
            name='shot_put_points',
            field=models.DecimalField(decimal_places=10, max_digits=10),
        ),
        migrations.AlterField(
            model_name='pentathlonresult',
            name='sum_all',
            field=models.DecimalField(decimal_places=10, max_digits=10),
        ),
    ]
