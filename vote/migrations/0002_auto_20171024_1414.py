# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-24 14:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apelectionmeta',
            options={'verbose_name_plural': 'AP election meta data'},
        ),
        migrations.AlterField(
            model_name='apelectionmeta',
            name='ballot_measure',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meta', to='election.BallotMeasure'),
        ),
        migrations.AlterField(
            model_name='apelectionmeta',
            name='election',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meta', to='election.Election'),
        ),
        migrations.AlterField(
            model_name='apelectionmeta',
            name='precincts_reporting',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='apelectionmeta',
            name='precincts_reporting_pct',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='apelectionmeta',
            name='precincts_total',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
