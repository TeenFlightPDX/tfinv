# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-05 17:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0003_auto_20170205_0925'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]