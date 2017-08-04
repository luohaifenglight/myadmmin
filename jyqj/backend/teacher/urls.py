#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from backend.accounts.perms import perm_required
from .views import teacher_list, teacher_edit, TeacherDTView, get_teacher_by_mobile, course_system_choices_v
teacher_urls = [
    url(r'^teacher_list/$', perm_required(['teacher.can_view'])(teacher_list), name='teacher_list'),
    url(r'^datatable/$', TeacherDTView.as_view(), name='datatable'),
    url(r'^get_teacher_name', get_teacher_by_mobile, name='teacher_name'),
    url(r'^teacher_list/teacher_create/$', perm_required(['teacher.can_create'])(teacher_edit), name='teacher_create'),
    url(r'^teacher_list/teacher_modify/(\d+)/$', perm_required(['teacher.can_modify'])(teacher_edit), name='teacher_modify'),
    url(r'^course_system_choices/$', course_system_choices_v, name='course_system_choices'),
    
]
