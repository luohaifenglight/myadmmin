#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.datatable import DTCols


LIST_FIELDS = DTCols([

    {'name': 'type', 'orderable': False},
    {'name': 'name', 'orderable': False},
    {'name': 'seq', 'orderable': False},
    {'name': 'sublevel_sum', 'orderable': False},
    {'name': 'operate', 'orderable': False},

])

QUERY_TYPE = [
    ('', u'全部'),
    ('id', u'id'),
    ('type', u'类型'),
]