# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-28 11:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='self_intro',
            new_name='about_me',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='reputation',
            new_name='honor',
        ),
    ]
