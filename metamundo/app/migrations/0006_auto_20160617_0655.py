# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-17 06:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20160617_0648'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='world',
            name='blob',
        ),
        migrations.AddField(
            model_name='blob',
            name='blob_coords',
            field=models.TextField(default='', max_length=10000),
        ),
        migrations.AddField(
            model_name='blob',
            name='world',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app.World'),
        ),
    ]