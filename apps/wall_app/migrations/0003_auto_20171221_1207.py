# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-21 17:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall_app', '0002_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(upload_to='documents/gifs'),
        ),
    ]
