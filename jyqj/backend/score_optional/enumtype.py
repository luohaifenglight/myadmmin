#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.datatable import DTCols
from utils.enumeration import Enumeration


LIST_FIELDS = DTCols([
    {'name': 'classify', 'orderable': False},
    {'name': 'name', 'orderable': False},
    {'name': 'score_num', 'orderable': False},
    {'name': 'id', 'orderable': False},
])

QUERY_TYPE = [
]

SCORE_OPTIONAL_TYPE = Enumeration([
    (0, 'select_homework', u'选弹作业'),
])
