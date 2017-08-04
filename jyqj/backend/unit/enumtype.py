#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.datatable import DTCols
from utils.enumeration import Enumeration
from .models import SectionAudioTeach, SectionVideoTeach, SectionSegmentPlay, \
    SectionFullPlay, SectionHomework, SectionGame


LIST_FIELDS = DTCols([
    {'name': 'id'},
    {'name': 'type', 'orderable': False},
    {'name': 'name', 'orderable': False},
    {'name': 'section_num', 'orderable': False},
    {'name': 'status', 'orderable': False},
    {'name': 'id', 'orderable': False},
])

SECTION_LIST_FIELDS = DTCols([
    {'name': 'seq', 'orderable': False},
    {'name': 'name', 'orderable': False},
    {'name': 'desc_type', 'orderable': False},
    {'name': 'section_id', 'orderable': False},
    {'name': 'type', 'visible': False},
    {'name': 'id', 'visible': False},
    {'name': 'is_current_use', 'visible': False},
])

QUERY_TYPE = [
    ('name', u'单元名称'),
]

UNIT_TYPE = Enumeration([
    (0, 'GCQ', u'歌唱曲'),
    (1, 'MC', u'模唱'),
    (2, 'TZYX', u'弹奏游戏'),
    (3, 'QNYD', u'全能乐队'),
    (4, 'XXYZJ', u'小小演奏家'),
    (5, 'YL', u'乐理'),
    (6, 'ZY_ZJ', u'作业／总结'),
    (7, 'jzdr', u'节奏达人'),
    (8, 'ZC', u'转场')
])

SECTION_TYPE = Enumeration([
    (0, 'YP', u'音频'),
    (1, 'SP', u'视频'),
    (2, 'MZ', u'模奏'),
    (3, 'GZ', u'跟奏'),
    (4, 'ZY', u'作业'),
    (5, 'YX', u'游戏'),
])

SECTION_TYPE_MODEL = [
    SectionAudioTeach, SectionVideoTeach, SectionSegmentPlay,
    SectionFullPlay, SectionHomework, SectionGame
]


SECTION_TYPE_TEMPLATE = [
    'section_audio_form.html',
    'section_video_form.html',
    'section_segment_form.html',
    'section_full_form.html',
    'section_homework_form.html',
    'section_game_form.html',
]

PLAY_WAY = Enumeration([
    (0, 'XXBF', u'循环播放'),
    (1, 'BFS', u'播放一次后停止'),
    (2, 'BFN', u'播放一次后直接进入下一环节'),
])

STAR_TYPE = Enumeration([
    (1, 'F', u'1星'),
    (2, 'S', u'2星'),
    (3, 'T', u'3星'),
    (4, 'F', u'4星'),
    (5, 'FI', u'5星'),

])

GAME_TYPE = Enumeration([
    (1, 'YYQQ', u'音乐气球'),
    (0, 'BKP', u'不靠谱'),

])

KEYBOARD_TYPE = Enumeration([
    ('100', 'UP', u'上键盘'),
    ('010', 'DOWN', u'下键盘'),
    ('001', 'FOOT', u'脚键盘'),
    ('110', 'UP_DOWN', u'上键盘+下键盘'),
    ('111', 'UP_DOWN_FOOT', u'上键盘+下键盘+脚键盘'),
])

