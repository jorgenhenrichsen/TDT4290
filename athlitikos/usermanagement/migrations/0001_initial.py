# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-19 10:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import usermanagement.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=100)),
                ('birth_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Judge',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='usermanagement.Person')),
                ('judge_level', models.CharField(choices=[('0', 'Level0'), ('1', 'Level1'), ('2', 'Level2'), ('3', 'Level3')], default=usermanagement.models.JudgeLevel(0), max_length=10)),
            ],
            bases=('usermanagement.person',),
        ),
        migrations.CreateModel(
            name='Lifter',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='usermanagement.Person')),
            ],
            bases=('usermanagement.person',),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='usermanagement.Person')),
            ],
            bases=('usermanagement.person',),
        ),
    ]
