#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from backend.accounts.perms import perm_required
from .views import score_enjoy_modify, score_enjoy_list, ScoreEnjoyDTView, score_enjoy_manage_list, \
    ScoreEnjoyManageDTView, score_enjoy_manage_modify, score_enjoy_office_choices_v

score_enjoy_urls = [
    url(r'^score_enjoy_list/$', perm_required(['score_optional.can_view'])(score_enjoy_list), name='score_enjoy_list'),
    url(r'^datatable/$', ScoreEnjoyDTView.as_view(), name='datatable'),
    url(r'^score_enjoy_modify/$', perm_required(['score_optional.can_modify'])(score_enjoy_modify),
        name='score_enjoy_modify'),

    url(r'^score_enjoy_office_choices/$', score_enjoy_office_choices_v, name='score_enjoy_office_choices'),

    url(r'^score_enjoy_manage_list/$', perm_required(['score_optional.can_view'])(score_enjoy_manage_list),
        name='score_enjoy_manage_list'),
    url(r'^manage_datatable/$', ScoreEnjoyManageDTView.as_view(), name='mange_datatable'),
    url(r'^score_enjoy_manage_modify/(\d+)/$', perm_required(['score_optional.can_modify'])(score_enjoy_manage_modify),
        name='score_enjoy_manage_modify'),

]
