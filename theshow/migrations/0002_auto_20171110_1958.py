# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-10 19:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0005_auto_20171110_1458'),
        ('geography', '0001_initial'),
        ('entity', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('theshow', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('body', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='entity.Body')),
                ('division_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geography.DivisionLevel')),
                ('election_day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.ElectionDay')),
                ('jurisdiction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entity.Jurisdiction')),
                ('model_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('office', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='entity.Office')),
            ],
        ),
        migrations.AddField(
            model_name='pagecontent',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='theshow.PageContent'),
        ),
        migrations.AlterUniqueTogether(
            name='pagetype',
            unique_together=set([('model_type', 'election_day', 'division_level', 'jurisdiction', 'body', 'office')]),
        ),
    ]