# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-10 23:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rents', '0003_auto_20181109_2007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prop',
            name='title',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='reservationDate',
        ),
        migrations.RemoveField(
            model_name='reservationdate',
            name='checkIn',
        ),
        migrations.RemoveField(
            model_name='reservationdate',
            name='checkOut',
        ),
        migrations.AddField(
            model_name='reservation',
            name='ReservationDate',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='reservationdate',
            name='reservation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='rents.Reservation'),
        ),
    ]