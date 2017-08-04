#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.datatable import DTCols
from utils.enumeration import Enumeration



#＝＝＝＝＝＝＝＝＝＝＝＝欣赏曲库列表＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
LIST_FIELDS = DTCols([
    {'name': 'id', 'orderable': False},
    {'name': 'name', 'orderable': False},
    {'name': 'opt', 'orderable': False},
    {'name': 'status', 'visible': False},

])

QUERY_TYPE = [
    ('name', u'欣赏曲目名称'),

]

SCORE_OPTIONAL_TYPE = Enumeration([
    (0, 'select_homework', u'选弹作业'),
])



#＝＝＝＝＝＝＝＝＝＝＝＝欣赏曲库管理列表＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

#score enjoy manage
SEM_LIST_FIELDS = DTCols([
    {'name': 'id', 'orderable': False},
    {'name': 'name', 'orderable': False},
    {'name': 'score_num', 'orderable': False},
    {'name': 'opt', 'orderable': False},
])

SEM_QUERY_TYPE = [
]

SEM_SCORE_OPTIONAL_TYPE = Enumeration([
    (0, 'select_homework', u'选弹作业'),
])
