# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-25 15:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogues', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='manufacturer',
            options={'ordering': ['name'], 'verbose_name': 'Manufacturer, OEM (Original Equipment Manufacturer)', 'verbose_name_plural': 'Manufacturers, OEMs (Original Equipment Manufacturers)'},
        ),
    ]
