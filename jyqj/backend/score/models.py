#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from django.db import models
from backend.accounts.models import Admin


class Timbre(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'tb_timbre'


class Score(models.Model):
    admin = models.ForeignKey(Admin, blank=True, null=True)
    name = models.CharField(max_length=20)
    music_type = models.IntegerField(blank=True, null=True, default=0)
    music_category = models.IntegerField(blank=True, null=True, default=0)
    score_type = models.IntegerField(blank=True, null=True, default=0)
    ratio = models.IntegerField(blank=True, null=True, default=0)
    keyboard = models.CharField(max_length=3, default='000')
    xml_name = models.CharField(max_length=20)
    xml_path = models.CharField(max_length=100)
    b00_name = models.CharField(max_length=20)
    b00_path = models.CharField(max_length=100)
    b00_syx = models.CharField(max_length=200)
    tempo = models.IntegerField(default=40)
    sample_midi_name = models.CharField(max_length=20)
    sample_midi_path = models.CharField(max_length=100)
    compare_midi_name = models.CharField(max_length=20)
    compare_midi_path = models.CharField(max_length=100)
    sample_audio_name = models.CharField(max_length=20, blank=True, null=True)
    sample_audio_path = models.CharField(max_length=100, blank=True, null=True)
    is_weak = models.IntegerField(default=0)
    weak_type = models.IntegerField(default=0)
    is_repeat = models.IntegerField(default=0)
    poster_name = models.CharField(max_length=20, blank=True, null=True)
    poster_path = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    create_time = models.BigIntegerField(default=time.time())
    timbre = models.ManyToManyField(Timbre, through='ScoreTimbre', verbose_name=u'包含音色',
                                    related_name='scores')

    status = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_score'


class ScoreTimbre(models.Model):
    score = models.ForeignKey(Score)
    timbre = models.ForeignKey(Timbre)

    class Meta:
        auto_created = True
        db_table = 'tb_score_timbre'


class ScoreSegment(models.Model):
    score = models.ForeignKey(Score, related_name='score_segments')
    start = models.IntegerField()
    end = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(default=0)
    label = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'tb_score_segment'


class ScorePic(models.Model):
    score = models.ForeignKey(Score, related_name='score_images')
    pic_name = models.CharField(max_length=20)
    pic_path = models.CharField(max_length=100)
    seq = models.IntegerField()

    class Meta:
        db_table = 'tb_score_pic'


class QnydScore(models.Model):
    whole_score = models.ForeignKey(Score)
    staff1_score = models.ForeignKey(Score)
    staff2_score = models.ForeignKey(Score)
    staff3_score = models.ForeignKey(Score)
    name = models.CharField(max_length=20)
    staff1_name = models.CharField(max_length=10)
    staff2_name = models.CharField(max_length=10)
    staff3_name = models.CharField(max_length=10)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'tb_hzq_score'


