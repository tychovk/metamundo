# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-09 21:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20160709_1941'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='world',
            name='world_register',
        ),
        migrations.DeleteModel(
            name='WorldRegister',
        ),
    ]