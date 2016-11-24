# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-11-21 15:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('giftchange', '0010_auto_20161121_1828'),
    ]

    operations = [
        migrations.AddField(
            model_name='gift',
            name='isExchange',
            field=models.BooleanField(default=True, verbose_name='是否为交换礼物'),
        ),
        migrations.AlterField(
            model_name='gift',
            name='description',
            field=models.TextField(max_length=1000, verbose_name='礼物描述'),
        ),
    ]