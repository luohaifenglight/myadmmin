#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from backend.accounts.perms import perm_required
from .views import video_list, video_edit, VideoDTView, reset_status, video_choices, segment_choices, video_delete
video_urls = [
    url(r'^video_list/$', perm_required(['video.can_view'])(video_list), name='video_list'),
    url(r'^datatable/$', VideoDTView.as_view(), name='datatable'),
    url(r'^video_list/video_create/$', perm_required(['video.can_create'])(video_edit), name='video_create'),
    url(r'^video_list/video_modify/(\d+)/$', perm_required(['video.can_modify'])(video_edit), name='video_modify'),
    url(r'^reset_status/$', reset_status, name='reset_status'),
    url(r'^video_delete/$', video_delete, name='video_delete'),
    url(r'^choices/$', video_choices, name='choices'),
    url(r'^segment_choices/$', segment_choices, name='segment_choices'),
]
