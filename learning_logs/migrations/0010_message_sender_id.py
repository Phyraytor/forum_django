# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-10-17 07:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0009_auto_20181017_1012'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='sender_id',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
    ]
