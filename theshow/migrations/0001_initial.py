# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-02 13:01
from __future__ import unicode_literals

import core.aws
from django.db import migrations, models
import django.db.models.deletion
import theshow.models.person_image
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('entity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('tag', models.SlugField()),
                ('image', models.ImageField(storage=core.aws.StorageService(), upload_to=theshow.models.person_image.person_image_path)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='entity.Person')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='personimage',
            unique_together=set([('person', 'tag')]),
        ),
    ]
