# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-22 18:02
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import resultregistration.enums
import resultregistration.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('club_name', models.CharField(max_length=100, verbose_name='Navn')),
                ('region', models.CharField(blank=True, max_length=100, null=True, verbose_name='Region')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='Adresse')),
            ],
        ),
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competition_category', models.CharField(blank=True, choices=[('Nordisk Ungdom', 'Nordisk_ungdom'), ('EM', 'em'), ('Klubbmesterskap', 'klubbmesterskap'), ('Klubbstevne', 'klubbstevne'), ('Kretsmesterskap', 'kretsmesterskap'), ('Lagseriestevne', 'lagseriestevne'), ('Nasjonalt stevne', 'nasjonalt_stevne'), ('NM', 'nm'), ('NM-Junior', 'nm_junior'), ('NM-Senior', 'nm_senior'), ('NM-Ungdom', 'nm_ungdom'), ('NM-Veteran', 'nm_veteran'), ('Nordisk Junior', 'nordisk_junior'), ('Nordisk Senior', 'nordisk_senior'), ('Norgescup', 'norges_cup'), ('OL', 'ol'), ('Seriestevne', 'seriestevne'), ('VM', 'vm')], max_length=100, null=True, verbose_name='Kategori')),
                ('host', models.CharField(blank=True, max_length=100, null=True, verbose_name='Arrangør')),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('start_date', models.DateField(blank=True, help_text='år-måned-dag', null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_number', models.IntegerField()),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('Godkjent', 'approved'), ('Ikke godkjent', 'denied'), ('Ikke sendt', 'not_sent'), ('Til godkjenning', 'pending')], default='Ikke sendt', max_length=30)),
                ('secretary', models.CharField(blank=True, max_length=100, null=True, verbose_name='Sekretær')),
                ('speaker', models.CharField(blank=True, max_length=100, null=True, verbose_name='Taler')),
                ('notes', models.CharField(blank=True, max_length=300, null=True)),
                ('records_description', models.CharField(blank=True, max_length=300, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resultregistration.Competition')),
            ],
        ),
        migrations.CreateModel(
            name='InternationalGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_number', models.IntegerField()),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('Godkjent', 'approved'), ('Ikke godkjent', 'denied'), ('Ikke sendt', 'not_sent'), ('Til godkjenning', 'pending')], default=resultregistration.enums.Status('Ikke sendt'), max_length=30)),
                ('notes', models.CharField(blank=True, max_length=300, null=True)),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resultregistration.Competition')),
            ],
        ),
        migrations.CreateModel(
            name='InternationalResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_weight', models.FloatField(null=True, verbose_name='Kroppsvekt')),
                ('age_group', models.CharField(choices=[('JM', 'junior_men'), ('JK', 'junior_women'), ('M1', 'master_men_35'), ('M2', 'master_men_40'), ('M3', 'master_men_45'), ('M4', 'master_men_50'), ('M5', 'master_men_55'), ('M6', 'master_men_60'), ('M7', 'master_men_65'), ('M8', 'master_men_70'), ('M9', 'master_men_75'), ('K1', 'master_women_35'), ('K2', 'master_women_40'), ('K3', 'master_women_45'), ('K4', 'master_women_50'), ('K5', 'master_women_55'), ('K6', 'master_women_60'), ('K7', 'master_women_65'), ('K8', 'master_women_70'), ('K9', 'master_women_75'), ('SM', 'senior_men'), ('SK', 'senior_women'), ('UM', 'youth_men'), ('UK', 'youth_women')], max_length=20, null=True, verbose_name='Kategori')),
                ('weight_class', models.CharField(max_length=10, null=True, verbose_name='Vektklasse')),
                ('sinclair_coefficient', models.FloatField(blank=True, db_column='sinclair_coefficient', null=True)),
                ('veteran_coefficient', models.FloatField(blank=True, db_column='melzer_faber_coefficient', null=True)),
                ('age', models.IntegerField(null=True)),
                ('total_lift', models.IntegerField(blank=True, null=True, verbose_name='Total poeng')),
                ('points_with_sinclair', models.FloatField(blank=True, null=True, verbose_name='Poeng med sinclair')),
                ('points_with_veteran', models.FloatField(blank=True, null=True, verbose_name='Veteranpoeng')),
            ],
        ),
        migrations.CreateModel(
            name='MelzerFaber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField(verbose_name='Alder')),
                ('coefficient', models.FloatField(verbose_name='Koeffisient')),
                ('year', models.IntegerField(verbose_name='Årstall')),
            ],
        ),
        migrations.CreateModel(
            name='MoveAttempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('move_type', models.CharField(choices=[('Clean and jerk', 'clean_and_jerk'), ('Snatch', 'snatch')], max_length=20)),
                ('attempt_num', models.IntegerField(validators=[django.core.validators.MaxValueValidator(3), django.core.validators.MinValueValidator(1)])),
                ('weight', models.IntegerField()),
                ('success', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='OldPentathlonResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age_group', models.CharField(blank=True, max_length=20, null=True)),
                ('shot_put', models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True)),
                ('shot_put_points', models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True)),
                ('forty_meter', models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True)),
                ('forty_meter_points', models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True)),
                ('jump', models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True)),
                ('jump_points', models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True)),
                ('sum_all', models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True)),
                ('competition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resultregistration.Competition')),
            ],
        ),
        migrations.CreateModel(
            name='OldResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight_class', models.CharField(max_length=10, null=True, verbose_name='Vektklasse')),
                ('age_group', models.CharField(max_length=5, null=True, verbose_name='Kategori')),
                ('body_weight', models.FloatField(null=True, verbose_name='Kroppsvekt')),
                ('best_press', models.FloatField(blank=True, null=True, verbose_name='Press')),
                ('best_snatch', models.FloatField(blank=True, null=True, verbose_name='Rykk')),
                ('best_clean_and_jerk', models.FloatField(blank=True, null=True, verbose_name='Støt')),
                ('total_lift', models.FloatField(blank=True, null=True, verbose_name='Sammenlagt')),
                ('points_with_sinclair', models.FloatField(blank=True, null=True, verbose_name='Poeng')),
                ('sinclair_coefficient', models.FloatField(blank=True, null=True, verbose_name='Koeffisient')),
                ('competition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resultregistration.Competition')),
            ],
        ),
        migrations.CreateModel(
            name='PentathlonResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shot_put', models.DecimalField(decimal_places=5, max_digits=10)),
                ('shot_put_points', models.DecimalField(decimal_places=5, max_digits=10)),
                ('forty_meter', models.DecimalField(decimal_places=5, max_digits=10)),
                ('forty_meter_points', models.DecimalField(decimal_places=5, max_digits=10)),
                ('jump', models.DecimalField(decimal_places=5, max_digits=10)),
                ('jump_points', models.DecimalField(decimal_places=5, max_digits=10)),
                ('sum_all', models.DecimalField(decimal_places=5, max_digits=10)),
                ('competition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resultregistration.Competition')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=40, validators=[resultregistration.validators.validate_name], verbose_name='Fornavn')),
                ('last_name', models.CharField(max_length=100, validators=[resultregistration.validators.validate_name], verbose_name='Etternavn')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_weight', models.FloatField(null=True, verbose_name='Kroppsvekt')),
                ('age_group', models.CharField(choices=[('JM', 'junior_men'), ('JK', 'junior_women'), ('M1', 'master_men_35'), ('M2', 'master_men_40'), ('M3', 'master_men_45'), ('M4', 'master_men_50'), ('M5', 'master_men_55'), ('M6', 'master_men_60'), ('M7', 'master_men_65'), ('M8', 'master_men_70'), ('M9', 'master_men_75'), ('K1', 'master_women_35'), ('K2', 'master_women_40'), ('K3', 'master_women_45'), ('K4', 'master_women_50'), ('K5', 'master_women_55'), ('K6', 'master_women_60'), ('K7', 'master_women_65'), ('K8', 'master_women_70'), ('K9', 'master_women_75'), ('SM', 'senior_men'), ('SK', 'senior_women'), ('UM', 'youth_men'), ('UK', 'youth_women')], max_length=20, null=True, verbose_name='Kategori')),
                ('weight_class', models.CharField(max_length=10, null=True, verbose_name='Vektklasse')),
                ('sinclair_coefficient', models.FloatField(blank=True, db_column='sinclair_coefficient', null=True)),
                ('veteran_coefficient', models.FloatField(blank=True, db_column='melzer_faber_coefficient', null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('total_lift', models.IntegerField(blank=True, null=True, verbose_name='Total poeng')),
                ('points_with_sinclair', models.FloatField(blank=True, null=True, verbose_name='Poeng med sinclair')),
                ('points_with_veteran', models.FloatField(blank=True, null=True, verbose_name='Veteranpoeng')),
                ('best_clean_and_jerk', models.ForeignKey(blank=True, db_column='best_clean_and_jerk', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='best_clean_and_jerk', to='resultregistration.MoveAttempt')),
                ('best_snatch', models.ForeignKey(blank=True, db_column='best_snatch', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='best_snatch', to='resultregistration.MoveAttempt')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resultregistration.Group')),
                ('lifter_club', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resultregistration.Club')),
            ],
        ),
        migrations.CreateModel(
            name='Sinclair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('K', 'female'), ('M', 'male')], max_length=10, verbose_name='Kjønn')),
                ('sinclair_b', models.FloatField(verbose_name='b')),
                ('sinclair_A', models.FloatField(verbose_name='A')),
                ('year', models.IntegerField(verbose_name='Årstall')),
            ],
        ),
        migrations.CreateModel(
            name='Judge',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resultregistration.Person')),
                ('judge_level', models.CharField(choices=[('F', 'forbundsdommer'), ('Int. I', 'internasjonal_kategori_1'), ('Int. II', 'internasjonal_kategori_2'), ('K', 'kretsdommer')], default=resultregistration.enums.JudgeLevel('K'), max_length=10)),
            ],
            bases=('resultregistration.person',),
        ),
        migrations.CreateModel(
            name='Lifter',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resultregistration.Person')),
                ('birth_date', models.DateField(null=True, verbose_name='Fødselsdato')),
                ('gender', models.CharField(choices=[('K', 'female'), ('M', 'male')], max_length=10, null=True, verbose_name='Kjønn')),
            ],
            bases=('resultregistration.person',),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resultregistration.Person')),
            ],
            bases=('resultregistration.person',),
        ),
        migrations.AlterUniqueTogether(
            name='sinclair',
            unique_together=set([('gender', 'sinclair_b', 'sinclair_A', 'year')]),
        ),
        migrations.AddField(
            model_name='person',
            name='club',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resultregistration.Club'),
        ),
        migrations.AddField(
            model_name='oldresults',
            name='lifter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resultregistration.Person'),
        ),
        migrations.AddField(
            model_name='oldresults',
            name='lifter_club',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resultregistration.Club'),
        ),
        migrations.AddField(
            model_name='oldpentathlonresult',
            name='lifter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resultregistration.Person'),
        ),
        migrations.AddField(
            model_name='oldpentathlonresult',
            name='result',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resultregistration.OldResults'),
        ),
        migrations.AddField(
            model_name='moveattempt',
            name='parent_result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resultregistration.Result'),
        ),
        migrations.AlterUniqueTogether(
            name='melzerfaber',
            unique_together=set([('age', 'coefficient', 'year')]),
        ),
        migrations.AddField(
            model_name='internationalresult',
            name='best_clean_and_jerk',
            field=models.ForeignKey(blank=True, db_column='best_clean_and_jerk', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='international_best_clean', to='resultregistration.MoveAttempt'),
        ),
        migrations.AddField(
            model_name='internationalresult',
            name='best_snatch',
            field=models.ForeignKey(blank=True, db_column='best_snatch', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='international_best_snatch', to='resultregistration.MoveAttempt'),
        ),
        migrations.AddField(
            model_name='internationalresult',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resultregistration.InternationalGroup', verbose_name='Pulje'),
        ),
        migrations.AddField(
            model_name='result',
            name='lifter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resultregistration.Lifter'),
        ),
        migrations.AddField(
            model_name='pentathlonresult',
            name='lifter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resultregistration.Lifter'),
        ),
        migrations.AlterUniqueTogether(
            name='moveattempt',
            unique_together=set([('parent_result', 'attempt_num', 'move_type')]),
        ),
        migrations.AddField(
            model_name='internationalresult',
            name='lifter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resultregistration.Lifter', verbose_name='Utøver'),
        ),
        migrations.AddField(
            model_name='internationalgroup',
            name='competitors',
            field=models.ManyToManyField(to='resultregistration.Lifter'),
        ),
        migrations.AddField(
            model_name='group',
            name='chief_marshall',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='groups_chief_marshall', to='resultregistration.Judge', verbose_name='Chief Marshall'),
        ),
        migrations.AddField(
            model_name='group',
            name='competition_leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='groups_competition_leader', to='resultregistration.Judge', verbose_name='Stevneleder'),
        ),
        migrations.AddField(
            model_name='group',
            name='competitors',
            field=models.ManyToManyField(blank=True, to='resultregistration.Lifter'),
        ),
        migrations.AddField(
            model_name='group',
            name='judges',
            field=models.ManyToManyField(blank=True, related_name='groups_judges', to='resultregistration.Judge'),
        ),
        migrations.AddField(
            model_name='group',
            name='jury',
            field=models.ManyToManyField(blank=True, default='', related_name='groups_juries', to='resultregistration.Judge', verbose_name='Jurie'),
        ),
        migrations.AddField(
            model_name='group',
            name='technical_controller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='groups_technical_controller', to='resultregistration.Judge', verbose_name='Teknisk kontrollør'),
        ),
        migrations.AddField(
            model_name='group',
            name='time_keeper',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='groups_time_keeper', to='resultregistration.Judge', verbose_name='Tidtaker'),
        ),
        migrations.AlterUniqueTogether(
            name='result',
            unique_together=set([('group', 'lifter')]),
        ),
        migrations.AlterUniqueTogether(
            name='group',
            unique_together=set([('group_number', 'competition')]),
        ),
    ]
