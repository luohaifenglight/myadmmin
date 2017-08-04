#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from backend.accounts.perms import perm_required
from .views import student_edit, student_list, StudentDTView, class_choices, class_move
student_urls = [
    url(r'^student_list/$', perm_required(['student.can_view'])(student_list), name='student_list'),
    url(r'^datatable/$', StudentDTView.as_view(), name='datatable'),
    url(r'^student_list/student_modify/(\d+)/$', perm_required(['student.can_modify'])(student_edit), name='student_modify'),
    url(r'^class_choices/$', class_choices, name='class_choices'),
    url(r'^class_move/$', class_move, name='class_move'),
]
