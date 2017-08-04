#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.datatable import DTCols
from utils.enumeration import Enumeration


LIST_FIELDS = DTCols([
    {'name': 'name', 'orderable': False},
    {'name': 'teacher__name', 'orderable': False},
    {'name': 'course_system__name', 'orderable': False},
    {'name': 'start_time', 'orderable': False},
    {'name': 'course_rate', 'orderable': False},
    {'name': 'id', 'orderable': False},
])


STUDENT_LIST_FIELDS = DTCols([
    {'name': 'name', 'orderable': False},
    {'name': 'mobile', 'orderable': False},
    {'name': 'id', 'orderable': False},
])

QUERY_TYPE = [
    ('teacher__name', u'教师姓名'),
    ('name', u'班级名称')
]

SCORE_OPTIONAL_TYPE = Enumeration([
    (0, 'select_homework', u'选弹作业'),
])

ADD_STUDENT_STATUS = Enumeration([
    (0, 'SCUESS', u'成功'),
    (-1, 'NOTEXIT', u'未结业'),
    (-2, 'REPEAT', u'重复添加'),
    (-3, 'FINSH', u'已结业的班级'),
    (-4, 'GREATER', u'超过9个'),
    (-5, 'EXPERENCE', u'非当前机构体验账号'),
    (-6, 'CLASSERROR', u'当前班级不能添加体验账号'),
    (-7, 'COMPLETE', u'已结业的班级不能添加学员'),
])
