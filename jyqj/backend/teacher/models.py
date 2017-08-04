#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from django.db import models
from backend.institution.models import City, Institution, CourseSystem


class Teacher(models.Model):
    institution = models.ForeignKey(Institution, verbose_name=u'机构', related_name='teachers')
    city = models.ForeignKey(City, verbose_name=u'城市')
    name = models.CharField(verbose_name=u'名称', max_length=20)
    gender = models.IntegerField(verbose_name=u'性别', default=0)
    mobile = models.CharField(verbose_name=u'电话', max_length=20)
    password = models.CharField(verbose_name=u'密码', max_length=200)
    school_area = models.CharField(verbose_name=u'学校区域', max_length=20)
    create_time = models.BigIntegerField(default=time.time())
    status = models.BooleanField(default=False)
    course_system = models.ManyToManyField(CourseSystem, through='TeacherCourseSystem', verbose_name=u'管理课程体系',
                                           related_name='teachers')

    class Meta:
        db_table = 'tb_teacher'


class TeacherCourseSystem(models.Model):
    teacher = models.ForeignKey(Teacher)
    course_system = models.ForeignKey(CourseSystem)

    class Meta:
        auto_created = True
        db_table = 'tb_teacher_course_system'
