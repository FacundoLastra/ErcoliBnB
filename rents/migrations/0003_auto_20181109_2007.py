# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-09 23:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rents', '0002_auto_20181108_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservationdate',
            name='checkIn',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='reservationdate',
            name='checkOut',
            field=models.DateField(blank=True, null=True),
        ),
    ]