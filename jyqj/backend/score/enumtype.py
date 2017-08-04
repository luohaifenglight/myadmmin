#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.datatable import DTCols
from utils.enumeration import Enumeration


LIST_FIELDS = DTCols([
    {'name': 'id'},
    {'name': 'name', 'orderable': False},
    {'name': 'music_category', 'orderable': False},
    {'name': 'ratio', 'orderable': False},
    {'name': 'admin__user__username', 'orderable': False},
    {'name': 'create_time', 'orderable': False},
    {'name': 'status', 'orderable': False},
    {'name': 'id', 'orderable': False},
    {'name': 'music_type', 'visible': False},
])

QUERY_TYPE = [
    ('name', u'乐曲名称'),
]

MUSIC_CATEGORY_TYPE = Enumeration([
    (0, 'EG', u'儿歌'),
    (1, 'JDGQQ', u'经典歌唱曲'),
    (2, 'LXQ', u'流行曲子'),
])

SCORE_TYPE = Enumeration([
    (0, 'WXP', u'五线谱'),
    (1, 'DXP', u'单线谱'),
])

MUSIC_TYPE = Enumeration([
    (0, 'DZ', u'独奏'),
    (1, 'HZ', u'合奏'),
])

WEAK_TYPE = Enumeration([
    (0, 'NO', u'无弱起'),
    (1, 'ONE', u'弱起1拍'),
    (2, 'TWO', u'弱起2拍'),
    (3, 'THREE', u'弱起3拍'),
    (4, 'FOUR', u'弱起4拍'),
    (5, 'FIVE', u'弱起5拍'),
])

ERROR_MESSAGE = {
    -101: 'compare midi和sample midi小节数必须一致',
    -102: '配置的乐段小节数不能超过compare midi的小节数',
    -103: '上传的曲子最多支持2个part，且part数<=staff数',
}
