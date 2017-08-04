#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from django.db import models
from backend.institution.models import CourseSystem
from backend.score.models import Score


class ScoreOptional(models.Model):

    score = models.ForeignKey(Score, blank=True, null=True)
    type = models.IntegerField()
    seq = models.IntegerField()
    course_system = models.ForeignKey(CourseSystem, blank=True, null=True, related_name='score_optional')

    class Meta:
        db_table = 'tb_score_optional'
