#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.datatable import DTCols
from utils.enumeration import Enumeration


LIST_FIELDS = DTCols([
    {'name': 'id'},
    {'name': 'visitor_ip', 'orderable': False},
    {'name': 'visit_time'},
    {'name': 'operation_path', 'orderable': False},
    {'name': 'admin__user__username', 'orderable': False},
    {'name': 'action', 'orderable': False},
])

QUERY_TYPE = [
    ('operation_path', '操作路径'),
]

