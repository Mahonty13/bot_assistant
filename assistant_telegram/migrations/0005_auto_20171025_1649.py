# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 10:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistant_telegram', '0004_log_msg'),
    ]

    operations = [
        migrations.AddField(
            model_name='log_msg',
            name='intent',
            field=models.CharField(default=' ', max_length=200),
        ),
        migrations.AlterField(
            model_name='log_msg',
            name='msg',
            field=models.TextField(default=' ', max_length=200),
        ),
    ]