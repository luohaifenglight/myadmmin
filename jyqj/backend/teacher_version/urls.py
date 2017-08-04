#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from backend.accounts.perms import perm_required
from .views import teacherversion_list, teacherversion_edit, TeacherVersionDTView, reset_status
teacherversion_urls = [
    url(r'^teacherversion_list/$', perm_required(['teacherversion.can_view'])(teacherversion_list), name='teacherversion_list'),
    url(r'^datatable/$', TeacherVersionDTView.as_view(), name='datatable'),
    url(r'^teacherversion_list/teacherversion_create/$', perm_required(['teacherversion.can_create'])(teacherversion_edit), name='teacherversion_create'),
    url(r'^teacherversion_list/teacherversion_modify/(\d+)/$', perm_required(['teacherversion.can_modify'])(teacherversion_edit), name='teacherversion_modify'),
    url(r'^reset_status/$', reset_status, name='reset_status'),
]
