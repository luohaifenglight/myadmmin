#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from django.db import models


class TeacherVersion(models.Model):
    zip_path = models.CharField(verbose_name=u'视频路径', max_length=200)
    zip_name = models.CharField(verbose_name=u'缩略图路径', max_length=200)
    version = models.CharField(verbose_name=u'版本号', max_length=20)
    package_code = models.CharField(verbose_name=u'APP版本号', max_length=20)
    public_type = models.IntegerField(verbose_name=u'类型', default=0)
    version_type = models.IntegerField(verbose_name=u'类型', default=0)
    size = models.FloatField(verbose_name=u'大小')
    create_time = models.BigIntegerField(default=time.time())
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'tb_teacher_app_version'

