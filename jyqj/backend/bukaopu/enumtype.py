#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.datatable import DTCols
from utils.enumeration import Enumeration

# 填写数据库字段名称
LIST_FIELDS = DTCols([
    {'name': 'id'},
    {'name': 'name', 'orderable': False},
    {'name': 'element_num', 'orderable': False},
    {'name': 'status', 'orderable': False},
    {'name': 'opt', 'orderable': False},

])

QUERY_TYPE = [
    ('name', u'不靠谱图片管理'),
]

INSTITUTION_TYPE = Enumeration([
    (0, 'OFFICE', u'直营'),
    (1, 'BRANCH', u'非直营')
])

# 不靠谱 目标音频管理
TARGET_LIST_FIELDS = DTCols([
    {'name': 'name'},
    {'name': 'status', 'orderable': False},
    {'name': 'opt', 'orderable': False},

])

TARGET_QUERY_TYPE = [
    ('name', u'不靠谱图片管理'),
]

TARGET_TYPE = Enumeration([
    (0, 'OFFICE', u'直营'),
    (1, 'BRANCH', u'非直营')
])

# 关卡管理
LEVEL_LIST_FIELDS = DTCols([
    {'name': 'id'},
    {'name': 'type', 'orderable': False},
    {'name': 'target', 'orderable': False},
    {'name': 'name', 'orderable': False},
    {'name': 'seq', 'orderable': False},
    {'name': 'status', 'orderable': False},
    {'name': 'opt', 'orderable': False},
])

LEVEL_QUERY_TYPE = [
    ('name', u'不靠谱关卡管理'),
]

LEVEL_TYPE = Enumeration([
    (0, 'OFFICE', u'直营'),
    (1, 'BRANCH', u'非直营')
])


LEVEL_CATEGORY_TYPE = Enumeration([
    (0, 'OFFCOURSE', u'课后乐园'),
    (1, 'ONCOURSE', u'随堂游戏'),
])