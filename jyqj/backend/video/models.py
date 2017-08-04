#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from django.db import models
from backend.institution.models import City, Institution, CourseSystem


class Video(models.Model):
    video_path = models.CharField(verbose_name=u'视频路径', max_length=200)
    thumb_path = models.CharField(verbose_name=u'缩略图路径', max_length=200)
    name = models.CharField(verbose_name=u'名称', max_length=50)
    type = models.IntegerField(verbose_name=u'类型', default=0)
    size = models.FloatField(verbose_name=u'大小')
    time = models.FloatField(verbose_name=u'时长')
    suffix = models.CharField(verbose_name=u'后缀', max_length=20)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'tb_video'


class VideoSegment(models.Model):
    video = models.ForeignKey(Video, verbose_name=u'视频', related_name='video_segments')
    label = models.CharField(verbose_name=u'标签信息', max_length=20)
    start = models.FloatField(verbose_name=u'开始')
    end = models.FloatField(verbose_name=u'结束')

    class Meta:
        db_table = 'tb_video_segment'
