# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-10-18 09:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0013_auto_20181017_1357'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatsProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=50)),
                ('type_model', models.CharField(max_length=50)),
                ('type_engine', models.CharField(max_length=50)),
                ('type_drive', models.CharField(max_length=50)),
                ('year_create', models.BigIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learning_logs.Entry')),
            ],
        ),
    ]
