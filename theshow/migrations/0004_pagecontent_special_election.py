# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-29 18:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theshow', '0003_auto_20171115_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagecontent',
            name='special_election',
            field=models.BooleanField(default=False),
        ),
    ]
