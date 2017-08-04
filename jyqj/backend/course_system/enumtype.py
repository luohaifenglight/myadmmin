#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.datatable import DTCols
from utils.enumeration import Enumeration

LIST_FIELDS = DTCols([
    {'name': 'id', 'orderable': False},
    {'name': 'name', 'orderable': False},
    {'name': 'coordinate_num', 'orderable': False},

    {'name': 'course_num', 'orderable': False},
    {'name': 'id', 'orderable': False},
])

QUERY_TYPE = [
    ('name', u'课程体系名称')
]

SCORE_OPTIONAL_TYPE = Enumeration([
    (0, 'select_homework', u'选弹作业'),
])

COURSE_SYSTEM_TYPE = Enumeration([
    (0, 'RIGHT', u'正式'),
    (1, 'EXPERIENCE', u'体验')
])
