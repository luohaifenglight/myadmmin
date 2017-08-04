#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.datatable import DTCols
from utils.enumeration import Enumeration


LIST_FIELDS = DTCols([
    {'name': 'id'},
    {'name': 'type', 'orderable': False},
    {'name': 'name', 'orderable': False},
    {'name': 'size', 'orderable': False},
    {'name': 'time', 'orderable': False},
    {'name': 'suffix', 'orderable': False},
    {'name': 'status', 'orderable': False},
    {'name': 'id', 'orderable': False},
])

QUERY_TYPE = [
    ('name', u'名称'),
]

VIDEO_TYPE = Enumeration([
    (0, 'GCQ', u'导入／转场'),
    (1, 'JZ', u'乐理讲解'),
    (2, 'SXSF', u'音乐欣赏'),
    (3, 'LLJJ', u'教谱'),
    (4, 'YYDR', u'教奏'),
    (5, 'YYDR', u'示范'),
    (6, 'YYDR', u'跟唱'),
    (7, 'JC', u'教唱'),
])
