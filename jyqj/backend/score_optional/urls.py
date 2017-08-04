#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from backend.accounts.perms import perm_required
from .views import score_optional_edit, score_optional_list, ScoreOptionalDTView
score_optional_urls = [
    url(r'^score_optional_list/$', perm_required(['score_optional.can_view'])(score_optional_list), name='score_optional_list'),
    url(r'^datatable/$', ScoreOptionalDTView.as_view(), name='datatable'),
    url(r'^score_optional_list/score_optional_modify/(\d+)/$', perm_required(['score_optional.can_modify'])(score_optional_edit), name='score_optional_modify'),
    
]
