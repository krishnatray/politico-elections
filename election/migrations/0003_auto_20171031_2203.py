# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-31 22:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0002_auto_20171031_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidateelection',
            name='candidate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidate_elections', to='election.Candidate'),
        ),
        migrations.AlterField(
            model_name='candidateelection',
            name='election',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidate_elections', to='election.Election'),
        ),
    ]