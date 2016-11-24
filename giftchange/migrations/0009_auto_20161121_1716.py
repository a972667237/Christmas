# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-11-21 09:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('giftchange', '0008_auto_20161121_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='giftsystem_user',
            name='name',
            field=models.CharField(default='wueiz', max_length=100, verbose_name='名字'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='exchangegift',
            name='gift',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='giftchange.Gift'),
        ),
    ]