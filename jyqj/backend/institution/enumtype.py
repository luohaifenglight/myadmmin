#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.datatable import DTCols
from utils.enumeration import Enumeration


LIST_FIELDS = DTCols([
    {'name': 'id'},
    {'name': 'type', 'orderable': False},
    {'name': 'name', 'orderable': False},
    {'name': 'city__name', 'orderable': False},
    {'name': 'concurrent_num', 'orderable': False},
    {'name': 'create_time', 'orderable': False},
    {'name': 'status', 'orderable': False},
    {'name': 'id', 'orderable': False},

])


STUDENT_LIST_FIELDS = DTCols([
    {'name': 'name', 'orderable': False},
    {'name': 'mobile', 'orderable': False},
    {'name': 'id', 'orderable': False},
])

QUERY_TYPE = [
    ('name', u'机构名称'),
]

INSTITUTION_TYPE = Enumeration([
    (0, 'OFFICE', u'直营'),
    (1, 'BRANCH', u'非直营')
])
