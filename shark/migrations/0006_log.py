# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-17 19:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shark', '0005_auto_20160312_1651'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('url', models.CharField(max_length=1024)),
                ('referrer', models.CharField(blank=True, max_length=1024)),
                ('user_agent', models.CharField(blank=True, max_length=1024)),
                ('ip_address', models.GenericIPAddressField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
