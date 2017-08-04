#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.datatable import DTCols


LIST_FIELDS = DTCols([
    {'name': 'f1'},
    {'name': 'f2', 'orderable': False},
    {'name': 'f3', 'orderable': False},
    {'name': 'f4', 'orderable': False},
    {'name': 'f5', 'orderable': False}
])

QUERY_TYPE = [
    ('', u'全部'),
    ('f1', u'字段一'),
    ('f2', u'字段二'),
]