# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-26 07:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assistant_telegram', '0009_delete_undefined_msg'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='context_chat',
            name='chat_id',
        ),
        migrations.RemoveField(
            model_name='context_chat',
            name='intent',
        ),
        migrations.RemoveField(
            model_name='entity',
            name='chat',
        ),
        migrations.RemoveField(
            model_name='log',
            name='chat_id',
        ),
        migrations.RemoveField(
            model_name='log',
            name='intent',
        ),
        migrations.RemoveField(
            model_name='story_action',
            name='intent',
        ),
        migrations.RemoveField(
            model_name='story_entity',
            name='intent',
        ),
        migrations.RemoveField(
            model_name='story_msg',
            name='intent',
        ),
        migrations.DeleteModel(
            name='Chat_id',
        ),
        migrations.DeleteModel(
            name='Context_chat',
        ),
        migrations.DeleteModel(
            name='Entity',
        ),
        migrations.DeleteModel(
            name='Intent',
        ),
        migrations.DeleteModel(
            name='Log',
        ),
        migrations.DeleteModel(
            name='Story_action',
        ),
        migrations.DeleteModel(
            name='Story_entity',
        ),
        migrations.DeleteModel(
            name='Story_msg',
        ),
    ]