#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.datatable import DTCols
from utils.enumeration import Enumeration


LIST_FIELDS = DTCols([
    {'name': 'id'},
    {'name': 'name', 'orderable': False},
    {'name': 'mobile', 'orderable': False},
    {'name': 'city__name', 'orderable': False},
    {'name': 'school_area', 'orderable': False},
    {'name': 'create_time', 'orderable': False},
    {'name': 'status', 'orderable': False},
    {'name': 'id', 'orderable': False},
])

QUERY_TYPE = [
    ('', u'全部'),
    ('name', u'姓名'),
    ('mobile', u'手机号'),
]

GENDER_TYPE = Enumeration([
    (0, 'BOY', u'男'),
    (1, 'GIRL', u'女'),
])
