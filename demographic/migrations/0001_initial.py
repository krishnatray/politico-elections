# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-17 19:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('geography', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CensusEstimate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estimate', models.FloatField()),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='census_estimates', to='geography.Division')),
            ],
        ),
        migrations.CreateModel(
            name='CensusLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('aggregation', models.CharField(choices=[('s', 'Sum'), ('a', 'Average'), ('m', 'Median')], default='s', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='CensusTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series', models.CharField(choices=[('acs1', 'American Community Survey 1-year data profiles'), ('acs5', 'American Community Survey 5-year'), ('sf1', 'Decennial census, SF1'), ('sf3', 'Decennial census, SF3')], max_length=4)),
                ('year', models.CharField(max_length=4)),
                ('code', models.CharField(max_length=10)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CensusVariable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=4)),
                ('label', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variables', to='demographic.CensusLabel')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variables', to='demographic.CensusTable')),
            ],
        ),
        migrations.AddField(
            model_name='censuslabel',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='labels', to='demographic.CensusTable'),
        ),
        migrations.AddField(
            model_name='censusestimate',
            name='variable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estimates', to='demographic.CensusVariable'),
        ),
    ]
