# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-14 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailverify',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
