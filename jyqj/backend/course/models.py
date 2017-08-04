#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from django.db import models
from backend.institution.models import CourseSystem
from backend.unit.models import Unit


class Course(models.Model):
    course_system = models.ForeignKey(CourseSystem, related_name='courses')
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=20,)
    seq = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    keypoint_name = models.CharField(max_length=50)
    keypoint_path = models.CharField(max_length=100)

    class Meta:
        db_table = 'tb_course'


class CourseUnit(models.Model):
    course = models.ForeignKey(Course, related_name='courseunit')
    unit = models.ForeignKey(Unit)
    seq = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_course_unit'
