# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-27 20:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0010_area_weight'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='area',
            options={'ordering': ['weight', 'id'], 'verbose_name': 'Area', 'verbose_name_plural': 'Areas'},
        ),
        migrations.AlterField(
            model_name='area',
            name='area',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='measure_point',
            name='area',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='control.Area'),
        ),
    ]
