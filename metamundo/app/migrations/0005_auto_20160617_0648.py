# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-17 06:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20160617_0647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='world',
            name='blob',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Blob'),
        ),
    ]