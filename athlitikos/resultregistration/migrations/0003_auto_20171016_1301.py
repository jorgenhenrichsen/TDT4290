# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-16 11:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import resultregistration.enums


class Migration(migrations.Migration):

    dependencies = [
        ('resultregistration', '0002_auto_20171013_1157'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent', models.BooleanField(default=False, verbose_name='Sendt til godkjenning')),
                ('approved', models.CharField(choices=[('Godkjent', 'approved'), ('Ikke godkjent', 'denied'), ('Til godkjenning', 'pending')], default=resultregistration.enums.Status('Ikke godkjent'), max_length=20, verbose_name='Status')),
                ('group_number', models.IntegerField()),
                ('date', models.DateField()),
                ('competition_leader', models.CharField(max_length=100, verbose_name='Stevneleder')),
                ('jury', models.CharField(default='', max_length=500, verbose_name='Jurie')),
                ('secretary', models.CharField(max_length=100, verbose_name='Sekretær')),
                ('speaker', models.CharField(max_length=100, verbose_name='Taler')),
                ('notes', models.CharField(blank=True, max_length=300, null=True)),
                ('records_description', models.CharField(blank=True, max_length=300, null=True)),
                ('cheif_marshall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pending_chief_marshall', to='resultregistration.Judge', verbose_name='Chief Marshall')),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resultregistration.Competition')),
                ('competitors', models.ManyToManyField(to='resultregistration.Lifter')),
                ('judges', models.ManyToManyField(related_name='pending_judges', to='resultregistration.Judge')),
                ('technical_controller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pending_technical_controller', to='resultregistration.Judge', verbose_name='Teknisk kontrollør')),
                ('time_keeper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pending_time_keeper', to='resultregistration.Judge', verbose_name='Tidtaker')),
            ],
        ),
        migrations.CreateModel(
            name='PendingResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_weight', models.FloatField(null=True, verbose_name='Kroppsvekt')),
                ('age_group', models.CharField(choices=[('J', 'junior'), ('M', 'master'), ('S', 'senior'), ('U', 'youth')], max_length=20, null=True, verbose_name='Kategori')),
                ('weight_class', models.IntegerField(null=True, verbose_name='Vektklasse')),
                ('sinclair_coefficient', models.FloatField(blank=True, db_column='sinclair_coefficient', null=True)),
                ('veteran_coefficient', models.FloatField(blank=True, db_column='melzer_faber_coefficient', null=True)),
                ('age', models.IntegerField()),
                ('total_lift', models.IntegerField(blank=True, null=True, verbose_name='Total poeng')),
                ('points_with_sinclair', models.FloatField(blank=True, null=True, verbose_name='Poeng med sinclair')),
                ('points_with_veteran', models.FloatField(blank=True, null=True, verbose_name='Veteranpoeng')),
                ('best_clean_and_jerk', models.ForeignKey(blank=True, db_column='best_clean_and_jerk', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pending_best_clean_and_jerk', to='resultregistration.MoveAttempt')),
                ('best_snatch', models.ForeignKey(blank=True, db_column='best_snatch', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pending_best_snatch', to='resultregistration.MoveAttempt')),
            ],
        ),
        migrations.AlterField(
            model_name='group',
            name='cheif_marshall',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chief_marshall', to='resultregistration.Judge', verbose_name='Chief Marshall'),
        ),
        migrations.AlterField(
            model_name='group',
            name='competition_leader',
            field=models.CharField(max_length=100, verbose_name='Stevneleder'),
        ),
        migrations.RemoveField(
            model_name='group',
            name='jury',
        ),
        migrations.AddField(
            model_name='group',
            name='jury',
            field=models.CharField(default='', max_length=500, verbose_name='Jurie'),
        ),
        migrations.AlterField(
            model_name='group',
            name='secretary',
            field=models.CharField(max_length=100, verbose_name='Sekretær'),
        ),
        migrations.AlterField(
            model_name='group',
            name='speaker',
            field=models.CharField(max_length=100, verbose_name='Taler'),
        ),
        migrations.AlterField(
            model_name='group',
            name='technical_controller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='technical_controller', to='resultregistration.Judge', verbose_name='Teknisk kontrollør'),
        ),
        migrations.AlterField(
            model_name='group',
            name='time_keeper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_keeper', to='resultregistration.Judge', verbose_name='Tidtaker'),
        ),
        migrations.AddField(
            model_name='pendingresult',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resultregistration.Group'),
        ),
        migrations.AddField(
            model_name='pendingresult',
            name='lifter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resultregistration.Lifter'),
        ),
        migrations.AlterUniqueTogether(
            name='pendinggroup',
            unique_together=set([('group_number', 'competition')]),
        ),
    ]