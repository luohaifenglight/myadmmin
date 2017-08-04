#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from django.db import models

class BalloonLevel(models.Model):
    # id = models.IntegerField(verbose_name=u'关卡分类',default=0)
    name = models.CharField(verbose_name=u'大关名字', max_length=20)
    type = models.IntegerField(verbose_name=u'关卡分类', default=0)
    seq = models.IntegerField(verbose_name=u'关卡序号', default=0)

    class Meta:
        db_table = 'tb_balloon_level'


class BalloonSubLevel(models.Model):
    # id = models.IntegerField( verbose_name=u'当前关卡主键',auto_created=True,primary_key=True)
    level_id = models.IntegerField( verbose_name=u'所属大关id')

    name = models.CharField(verbose_name=u'小关名字', max_length=20)
    seq = models.IntegerField(verbose_name=u'关卡分类', default=0)
    description = models.CharField(verbose_name=u'小关描述', max_length=200)
    pitch_rate = models.IntegerField(verbose_name=u'关卡分类', default=0)
    sing_rate = models.IntegerField(verbose_name=u'关卡分类', default=0)
    score_rate = models.IntegerField(verbose_name=u'关卡分类', default=0)
    hint_rate = models.IntegerField(verbose_name=u'关卡分类', default=0)
    pop_interval = models.IntegerField(verbose_name=u'关卡分类', default=0)
    fly_time = models.IntegerField(verbose_name=u'关卡分类', default=0)
    level_time = models.IntegerField(verbose_name=u'关卡分类', default=0)
    bgm_name = models.CharField(verbose_name=u'背景音乐名称', max_length=20)
    bgm_path = models.CharField(verbose_name=u'背景音乐地址', max_length=100)
    bgp_name = models.CharField(verbose_name=u'背景图片名称', max_length=20)
    bgp_path = models.CharField(verbose_name=u'背景图片地址', max_length=100)

    # lock_status = models.IntegerField(verbose_name=u'关卡分类', default=0)
    status = models.IntegerField(verbose_name=u'关卡分类', default=0)



    class Meta:
        db_table = 'tb_balloon_sub_level'



class BalloonSubLevelOctave(models.Model):

    sub_level_id = models.IntegerField(verbose_name=u'所属关卡id', default=0)
    octave_type = models.CharField(verbose_name=u'音域类型', max_length=5)
    keyboard = models.CharField(verbose_name=u'键盘类型', max_length=3)
    c = models.IntegerField(verbose_name=u'c占比', default=0)
    d = models.IntegerField(verbose_name=u'd占比', default=0)
    e = models.IntegerField(verbose_name=u'e占比', default=0)
    f = models.IntegerField(verbose_name=u'f占比', default=0)
    g = models.IntegerField(verbose_name=u'g占比', default=0)
    a = models.IntegerField(verbose_name=u'a占比', default=0)
    b = models.IntegerField(verbose_name=u'b占比', default=0)

    class Meta:
        db_table = 'tb_balloon_octave'
