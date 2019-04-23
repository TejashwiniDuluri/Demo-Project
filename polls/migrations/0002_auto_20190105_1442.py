# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-05 09:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='test',
            old_name='test_chap',
            new_name='chapter',
        ),
        migrations.RenameField(
            model_name='test',
            old_name='test_chapter',
            new_name='topic',
        ),
        migrations.AddField(
            model_name='test',
            name='sl_no',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]