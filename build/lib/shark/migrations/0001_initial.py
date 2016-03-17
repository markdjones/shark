# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-02 20:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EditableText',
            fields=[
                ('name', models.CharField(max_length=128, primary_key=True, serialize=False, unique=True)),
                ('content', models.TextField()),
                ('filename', models.CharField(max_length=1024)),
                ('handler_name', models.CharField(max_length=512)),
                ('line_nr', models.IntegerField()),
                ('last_used', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
