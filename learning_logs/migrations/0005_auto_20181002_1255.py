# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-10-02 09:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0004_entry_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='img',
            field=models.CharField(max_length=200),
        ),
    ]
