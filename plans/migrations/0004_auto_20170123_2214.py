# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-24 06:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0003_auto_20170116_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step_note',
            name='date_created',
            field=models.DateField(auto_now_add=True),
        ),
    ]