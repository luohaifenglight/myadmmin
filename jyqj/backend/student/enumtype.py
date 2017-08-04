#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.datatable import DTCols
from utils.enumeration import Enumeration


LIST_FIELDS = DTCols([
    {'name': 'name', 'orderable': False},
    {'name': 'mobile', 'orderable': False},
    {'name': 'classes_name', 'orderable': False},
    {'name': 'coin_num', 'orderable': False},
    {'name': 'create_time', 'orderable': False},
    #{'name': 'create_teacher__name', 'orderable': False},
    {'name': 'id', 'orderable': False},
])

QUERY_TYPE = [
    ('name', u'学员姓名'),
    ('mobile', u'手机号')
]

CLASS_STATUS = Enumeration([
    (0, 'UNFINSH', u'未结业'),
    (1, 'FINSH', u'已结业')
])


COMMAND_STATUS = Enumeration([
    (0, 'JIARU', u'加入'),
    (1, 'YICHU', u'移除'),
    (2, 'ZHUANRU', u'转入'),
    (3, 'ZHUANCHU', u'转出'),
])
