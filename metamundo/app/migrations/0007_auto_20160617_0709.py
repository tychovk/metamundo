# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-17 07:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20160617_0655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='world',
            name='world_coords',
            field=models.TextField(default='', max_length=10000, null=True),
        ),
    ]
