# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-31 16:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aspect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('score', models.IntegerField(default=0)),
                ('belt', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Future',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('future', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=30)),
                ('notes', models.CharField(max_length=200)),
                ('aspect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspects.Aspect')),
            ],
        ),
        migrations.CreateModel(
            name='Moment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moment', models.CharField(max_length=200)),
                ('plan', models.DateTimeField()),
                ('achieved', models.DateTimeField(null=True)),
                ('proof', models.ImageField(null=True, upload_to=b'')),
                ('aspect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspects.Aspect')),
            ],
        ),
    ]