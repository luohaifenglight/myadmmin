#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.datatable import DTCols
from utils.enumeration import Enumeration


LIST_FIELDS = DTCols([
    {'name': 'id'},
    {'name': 'public_type', 'orderable': False},
    {'name': 'version_type', 'orderable': False},
    {'name': 'package_code', 'orderable': False},
    {'name': 'version', 'orderable': False},
    {'name': 'size', 'orderable': False},
    {'name': 'create_time', 'orderable': False},
    {'name': 'zip_name', 'orderable': False},
    {'name': 'status', 'orderable': False},
    {'name': 'id', 'orderable': False},
])

QUERY_TYPE = [
    ('zip_name', u'名称'),
]

PUBLIC_TYPE = Enumeration([
    (0, 'DEBUG', u'debug'),
    (1, 'RELEASE', u'release'),
])

VERSION_TYPE = Enumeration([
    (0, 'BIG', u'大版本'),
    (1, 'SMALL', u'小版本'),
])
