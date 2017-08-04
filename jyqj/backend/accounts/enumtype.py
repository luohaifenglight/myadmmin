# -*- coding: UTF-8 -*-

from utils.datatable import DTCols
from utils.enumeration import Enumeration


ADMIN_TYPE = Enumeration([
    (0, 'OFFICE', u'总部管理员'),
    (1, 'BRANCH', u'机构管理员')
])
# 行政办、财务部、产品部、运营部、内容研发部、渠道部、支持中心、机构
ADMIN_DEPARTMENT = Enumeration([
    (0, 'XINGZHENG', u'行政办'),
    (1, 'CAIWU', u'财务部'),
    (2, 'CHANPIN', u'产品部'),
    (3, 'YUNYING', u'运营部'),
    (4, 'YANFA', u'内容研发部'),
    (5, 'QUDAO', u'渠道部'),
    (6, 'ZHICHI', u'支持中心'),
    (7, 'JIGOU', u'机构'),
])

LIST_FIELDS = DTCols([
    {'name': 'user__id'},
    {'name': 'type', 'orderable': False},
    {'name': 'department', 'orderable': False},
    {'name': 'user__username', 'orderable': False},
    {'name': 'user__belong_groups__id', 'orderable': False},
    {'name': 'mobile', 'orderable': False},
    {'name': 'create_time', 'orderable': False},
    {'name': 'status', 'orderable': False},
    {'name': 'user__id', 'orderable': False},
])

QUERY_TYPE = [
    ('mobile', u'电话'),
]

ROLE_LIST_FIELDS = DTCols([
    {'name': 'id'},
    {'name': 'name', 'orderable': False},
    {'name': 'create_time', 'orderable': False},
    {'name': 'status', 'orderable': False},
    {'name': 'id', 'orderable': False},
])

ROLE_QUERY_TYPE = [
    ('name', u'角色名称'),
]
