# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-01 20:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=30)),
                ('receiver', models.CharField(max_length=30)),
                ('body', models.CharField(max_length=300)),
                ('date', models.CharField(max_length=130)),
            ],
        ),
    ]
