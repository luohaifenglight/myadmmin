#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from django.db import models
from backend.institution.models import CourseSystem


class CourseCoordinate(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    seq = models.IntegerField()
    course_system = models.ForeignKey(CourseSystem, blank=True, null=True, related_name='course_coordinate')

    class Meta:
        db_table = 'tb_course_coordinate'
