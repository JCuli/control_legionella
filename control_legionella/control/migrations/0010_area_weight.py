# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-26 17:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0009_measure_status_ok'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='weight',
            field=models.IntegerField(null=True),
        ),
    ]
