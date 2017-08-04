#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from backend.accounts.perms import perm_required
from .views import score_list, score_edit, ScoreDTView, timbre_choices_v, \
    music_office_choices_v, qnyd_score_edit, reset_status, segment_choices, all_choices_v, \
    hzq_office_choices_v, score_copy, score_delete
score_urls = [
    url(r'^score_list/$', perm_required(['score.can_view'])(score_list), name='score_list'),
    url(r'^datatable/$', ScoreDTView.as_view(), name='datatable'),
    url(r'^score_list/score_create/$', perm_required(['score.can_create'])(score_edit), name='score_create'),
    url(r'^score_list/score_modify/(\d+)/$', perm_required(['score.can_modify'])(score_edit), name='score_modify'),
    url(r'^score_list/qnyd_score_create/$', qnyd_score_edit, name='qnyd_score_create'),
    url(r'^score_list/qnyd_score_modify/(\d+)/$', qnyd_score_edit, name='qnyd_score_modify'),
    url(r'^timbre_choices/$', timbre_choices_v, name='timbre_choices'),
    url(r'^reset_status/$', reset_status, name='reset_status'),
    url(r'^score_delete/$', score_delete, name='score_delete'),
    url(r'^score_copy/$', score_copy, name='score_copy'),
    url(r'^music_office_choices/$', music_office_choices_v, name='music_office_choices'),
    url(r'^music_all_choices/$', all_choices_v, name='music_all_choices'),
    url(r'^hzq_choices/$', hzq_office_choices_v, name='music_hzq_choices'),
    url(r'^segment_choices/$', segment_choices, name='segment_choices'),
]
