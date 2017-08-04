#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from django.db import models
from backend.score.models import Score, ScoreSegment
from backend.score_enjoy.models import ScoreEnjoy
from backend.video.models import VideoSegment, Video


class Unit(models.Model):
    name = models.CharField(max_length=20)
    show_name = models.CharField(max_length=20)
    type = models.IntegerField(default=0)
    description = models.CharField(max_length=200, blank=True, null=True)
    status = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_unit'


class UnitSection(models.Model):
    unit = models.ForeignKey(Unit, related_name='sections')
    section_id = models.IntegerField()
    type = models.IntegerField(default=0)
    seq = models.IntegerField(default=0)

    @property
    def name(self):
        from .enumtype import SECTION_TYPE_MODEL
        try:
            print self.section_id
            section = SECTION_TYPE_MODEL[self.type].objects.get(id=self.section_id)
        except:
            import traceback
            traceback.print_exc()
        return section.section_name

    class Meta:
        db_table = 'tb_unit_section'


class SectionAudioTeach(models.Model):
    section_name = models.CharField(max_length=20)
    pic_name = models.CharField(max_length=20, blank=True, null=True)
    pic_path = models.CharField(max_length=100, blank=True, null=True)
    audio_name = models.CharField(max_length=20, blank=True, null=True)
    audio_path = models.CharField(max_length=255, blank=True, null=True)
    play_type = models.IntegerField(default=0)
    is_auto_play = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_section_audio_teach'


class SectionFullPlay(models.Model):
    score = models.ForeignKey(Score)
    section_name = models.CharField(max_length=20)

    class Meta:
        db_table = 'tb_section_full_play'


class SectionGame(models.Model):
    level_id = models.IntegerField()
    section_name = models.CharField(max_length=20)
    type = models.IntegerField()

    class Meta:
        db_table = 'tb_section_game'


class SectionHomework(models.Model):
    section_name = models.CharField(max_length=20)

    class Meta:
        db_table = 'tb_section_homework'


class HomeworkPractice(models.Model):
    section = models.ForeignKey(SectionHomework, related_name='sections')
    score = models.ForeignKey(Score)
    star_num = models.IntegerField()
    times = models.IntegerField()
    keyboard = models.CharField(max_length=3,)
    tempo = models.IntegerField(default=40)

    class Meta:
        db_table = 'tb_homework_practice'


class HomeworkMCPractice(models.Model):
    section = models.ForeignKey(SectionHomework, related_name='mc_sections')
    score_enjoy = models.ForeignKey(ScoreEnjoy)

    class Meta:
        db_table = 'tb_homework_mc_practice'


class SectionSegmentPlay(models.Model):
    video = models.ForeignKey(Video)
    # video_segment = models.ForeignKey(VideoSegment)
    video_segment_id = models.IntegerField(default=0)
    score = models.ForeignKey(Score)
    score_segment = models.ForeignKey(ScoreSegment, on_delete=models.DO_NOTHING)
    section_name = models.CharField(max_length=20)
    keyboard = models.CharField(max_length=3)
    tempo = models.IntegerField(default=40)

    class Meta:
        db_table = 'tb_section_segment_play'

    @property
    def video_segment(self):
        try:
            seg = VideoSegment.objects.get(id=self.video_segment_id)
        except:
            seg = None
        return seg


class SectionVideoTeach(models.Model):
    video = models.ForeignKey(Video)
    #video_segment = models.ForeignKey(VideoSegment, blank=True, null=True, )
    video_segment_id = models.IntegerField(default=0)
    section_name = models.CharField(max_length=50)
    poster_name = models.CharField(max_length=20, blank=True, null=True)
    poster_path = models.CharField(max_length=100, blank=True, null=True)
    back_poster_name = models.CharField(max_length=200, blank=True, null=True)
    back_poster_path = models.CharField(max_length=100, blank=True, null=True)
    play_type = models.IntegerField(blank=True, null=True)
    is_auto_play = models.IntegerField(default=0)
    b00_name = models.CharField(max_length=200)
    b00_path = models.CharField(max_length=200)
    b00_syx = models.CharField(max_length=200)
    program_change_midi_name = models.CharField(max_length=200)
    program_change_midi_path = models.CharField(max_length=200)

    class Meta:
        db_table = 'tb_section_video_teach'

    @property
    def video_segment(self):
        try:
            seg = VideoSegment.objects.get(id=self.video_segment_id)
        except:
            seg = None
        return seg

