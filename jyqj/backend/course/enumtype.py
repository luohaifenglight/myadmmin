#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.datatable import DTCols
from utils.enumeration import Enumeration


LIST_FIELDS = DTCols([
    {'name': 'id'},
    {'name': 'course_system__name', 'orderable': False},
    {'name': 'name', 'orderable': False},
    {'name': 'seq', 'orderable': False},
    {'name': 'status', 'orderable': False},
    {'name': 'id', 'orderable': False},
    {'name': 'course_system__id', 'visible': False},
])

QUERY_TYPE = [
    ('name', u'课程名称'),
]
