#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from django.db import models
from backend.institution.models import CourseSystem
from backend.score.models import Score
from django import forms


class CourseSystemPrivate(models.Model):
    name = models.CharField(verbose_name=u'课程体系', max_length=50)

    class Meta:
        db_table = 'tb_course_system'

class ScoreEnjoy(models.Model):
    '''
    欣赏曲库
    '''

    name = models.CharField(max_length=20)
    audio_name = models.CharField(max_length=20)
    audio_path = models.CharField(max_length=100)
    poster_name = models.CharField(max_length=20)
    poster_path = models.CharField(max_length=100)
    status = models.IntegerField()

    class Meta:
        db_table = 'tb_score_enjoy'


class ScoreEnjoyManage(models.Model):
    '''
    欣赏曲库管理
    '''
    # Id, score_id, type, seq, course_system_id

    # score_id = models.IntegerField()
    score = models.ForeignKey(ScoreEnjoy)
    type = models.IntegerField()
    seq = models.IntegerField()
    course_system = models.ForeignKey(CourseSystem, blank=True, null=True, related_name='score_enjoy')

    # course_system_id = models.IntegerField()

    class Meta:
        db_table = 'tb_score_enjoy_manage'
