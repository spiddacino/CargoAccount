# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-11 19:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NahcoTrack', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Banks',
            new_name='Bank',
        ),
    ]