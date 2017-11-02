# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-02 13:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demographic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='censusvariable',
            name='code',
            field=models.CharField(help_text="3 digit code for variable and 'E', e.g., 001E.", max_length=4),
        ),
    ]
