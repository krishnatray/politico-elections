# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-24 14:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0004_auto_20171018_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='division',
            name='effective_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='division',
            name='effective_start',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='geography',
            name='effective_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='geography',
            name='effective_start',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
