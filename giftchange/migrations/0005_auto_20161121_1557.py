# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-11-21 07:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('giftchange', '0004_auto_20161121_1224'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Wechat_user',
            new_name='GiftSystem_user',
        ),
        migrations.AlterField(
            model_name='changeresult',
            name='wangGiftType',
            field=models.CharField(choices=[('01', '食物'), ('02', '服装配饰'), ('03', '钟表首饰'), ('04', '化妆品'), ('05', '运动户外'), ('06', '电器数码'), ('07', '小玩意'), ('08', '手工物件'), ('09', '二次元'), ('10', '图书音像'), ('11', '学习资源'), ('12', '其它')], max_length=15, verbose_name='回礼类型'),
        ),
        migrations.AlterField(
            model_name='gift',
            name='type',
            field=models.CharField(choices=[('01', '食物'), ('02', '服装配饰'), ('03', '钟表首饰'), ('04', '化妆品'), ('05', '运动户外'), ('06', '电器数码'), ('07', '小玩意'), ('08', '手工物件'), ('09', '二次元'), ('10', '图书音像'), ('11', '学习资源'), ('12', '其它')], max_length=15, verbose_name='礼物类别'),
        ),
    ]
