#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from django.db import models


class Province(models.Model):
    name = models.CharField(verbose_name=u'省份名', max_length=50)

    class Meta:
        db_table = 'tb_province'


class City(models.Model):
    name = models.CharField(verbose_name=u'城市名', max_length=50)
    province = models.ForeignKey(Province, verbose_name=u'省份')

    class Meta:
        db_table = 'tb_city'


class CourseSystem(models.Model):
    name = models.CharField(verbose_name=u'课程体系', max_length=50)
    background_image_name = models.CharField(max_length=200)
    background_image_path = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    course_system_type = models.IntegerField(verbose_name=u'课程体系类型', default=0)

    class Meta:
        db_table = 'tb_course_system'


class Institution(models.Model):
    city = models.ForeignKey(City, verbose_name=u'城市')
    name = models.CharField(verbose_name=u'机构名称', max_length=20)
    code = models.CharField(verbose_name=u'简码', max_length=20)
    type = models.IntegerField(verbose_name=u'机构类型', default=0)
    concurrent_num = models.IntegerField(verbose_name=u'并发数', default=0)
    status = models.BooleanField(default=False)
    experience_student_num = models.IntegerField(verbose_name=u'体验学生数', default=0)
    create_time = models.BigIntegerField(default=time.time())
    course_system = models.ManyToManyField(CourseSystem, through='InstitutionCourseSystem', verbose_name=u'管理课程体系',
                                           related_name='institutions')

    class Meta:
        db_table = 'tb_institution'


class InstitutionCourseSystem(models.Model):
    Institution = models.ForeignKey(Institution)
    course_system = models.ForeignKey(CourseSystem)

    class Meta:
        auto_created = True
        db_table = 'tb_institution_course_system'

