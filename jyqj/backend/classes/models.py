#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from django.db import models
from backend.teacher.models import Teacher, CourseSystem
from backend.course.models import Course



class Class(models.Model):

    create_teacher = models.ForeignKey(Teacher, related_name='create_classes')
    teacher = models.ForeignKey(Teacher, related_name='classes')
    name = models.CharField(max_length=100)
    course_system = models.ForeignKey(CourseSystem, related_name='classes')
    start_time = models.BigIntegerField(default=int(time.time()))
    create_time = models.BigIntegerField(default=int(time.time()))
    course_rate = models.IntegerField(default=0)
    class_status = models.IntegerField(default=0)
    share_status = models.IntegerField(default=0)


    class Meta:
        db_table = 'tb_class'


class CourseClass(models.Model):
    classes = models.ForeignKey(Class, db_column='class_id', related_name='classess')
    course = models.ForeignKey(Course)
    teacher = models.ForeignKey(Teacher, blank=True, null=True)
    teach_time = models.BigIntegerField(blank=True, null=True)
    course_status = models.IntegerField()
    unit_id = models.IntegerField(blank=True, null=True)
    section_id = models.IntegerField(blank=True, null=True)
    section_type = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'tb_course_class'
