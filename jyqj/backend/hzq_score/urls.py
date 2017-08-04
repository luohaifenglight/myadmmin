#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from backend.accounts.perms import perm_required
from .views import score_list, HZQScoreDTView, hzq_score_edit
hzq_score_urls = [
    url(r'^hzq_score_list/$', score_list, name='hzq_score_list'),
    url(r'^datatable/$', HZQScoreDTView.as_view(), name='datatable'),
    url(r'^hzq_score_list/qnyd_score_create/$', hzq_score_edit, name='qnyd_score_create'),
    url(r'^hzq_score_list/qnyd_score_modify/(\d+)/$', hzq_score_edit, name='qnyd_score_modify'),
]
