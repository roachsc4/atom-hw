# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-20 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='state',
            field=models.CharField(choices=[('in_progress', 'In progress'), ('ready', 'Ready')], default='in_progress', max_length=12),
        ),
    ]