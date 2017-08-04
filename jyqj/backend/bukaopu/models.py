#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from django.db import models


class BKPLevel(models.Model):
    name = models.CharField(verbose_name=u'关卡名称', max_length=20)
    type = models.IntegerField(verbose_name=u'关卡分类', default=0)
    seq = models.IntegerField(verbose_name=u'关卡顺序', default=0)
    description = models.CharField(verbose_name=u'关卡描述', max_length=200)
    bgm_name = models.CharField(verbose_name=u'背景音乐名称', max_length=20)
    bgm_path = models.CharField(verbose_name=u'背景音乐地址', max_length=100)
    status = models.IntegerField(verbose_name=u'发布状态 0:课后乐园 1:随堂练习', default=0)

    class Meta:
        db_table = 'tb_bkp_level'


class BKPPic(models.Model):
    name = models.CharField(verbose_name=u'图片名称', max_length=20)
    element_num = models.IntegerField(verbose_name=u'包含元素数量', default=0)
    path = models.CharField(verbose_name=u'图片路径', max_length=100)
    description = models.CharField(verbose_name=u'图片描述', max_length=200)
    status = models.IntegerField(verbose_name=u'发布状态', default=0)

    class Meta:
        db_table = 'tb_bkp_pic'


class BKPRound(models.Model):
    bkp_level_id = models.IntegerField(verbose_name=u'所属关卡id', default=0)
    bkp_target_name = models.CharField(verbose_name=u'目标名称', max_length=100)
    time = models.IntegerField(verbose_name=u'轮次时间', default=0)
    seq = models.IntegerField(verbose_name=u'轮次编号', default=0)
    bkp_pic_id = models.IntegerField(verbose_name=u'图片id', default=0)

    class Meta:
        db_table = 'tb_bkp_round'


class BKPTarget(models.Model):
    bkp_pic_id = models.IntegerField(verbose_name=u'所属图片id', default=0)
    # todo 没有外按键关联
    # pic = models.ForeignKey(BKPPic, verbose_name=u'图片元素', related_name='pic_segment')

    name = models.CharField(verbose_name=u'目标名称', max_length=20)
    description = models.CharField(verbose_name=u'描述音频描述', max_length=200)
    top_left_x = models.IntegerField(verbose_name=u'左上x', default=0)
    top_left_y = models.IntegerField(verbose_name=u'左上y', default=0)
    bottom_right_x = models.IntegerField(verbose_name=u'右下x', default=0)
    bottom_right_y = models.IntegerField(verbose_name=u'右下y', default=0)
    target_audio_name = models.CharField(verbose_name=u'目标音频名称', max_length=100)
    target_audio_path = models.CharField(verbose_name=u'目标音频路径', max_length=255)
    desc_audio_name = models.CharField(verbose_name=u'描述音频名称', max_length=100)
    desc_audio_path = models.CharField(verbose_name=u'描述音频音频路径', max_length=100)

    class Meta:
        db_table = 'tb_bkp_target'


