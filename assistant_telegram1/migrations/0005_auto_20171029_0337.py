# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-28 21:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistant_telegram1', '0004_auto_20171029_0318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]