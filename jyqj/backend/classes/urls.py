#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from backend.accounts.perms import perm_required
from .views import class_edit, class_list, ClassDTView, remove_student, add_student, student_list, StudentDTView, teacher_choices_v, course_system_choices_v
class_urls = [
    url(r'^class_list/$', perm_required(['class.can_view'])(class_list), name='class_list'),
    url(r'^datatable/$', ClassDTView.as_view(), name='datatable'),
    url(r'^student/datatable/$', StudentDTView.as_view(), name='student_datatable'),
    url(r'^add_student/$', add_student, name='add_student'),
    url(r'^class_list/student_list/(\d+)/$', student_list, name='student_list'),
    url(r'^course_system_choices/$', course_system_choices_v, name='course_system_choices'),
    url(r'^teacher_choices/$', teacher_choices_v, name='teacher_choices'),
    url(r'^class_list/class_create/$', perm_required(['class.can_modify'])(class_edit), name='class_create'),
    url(r'^remove_student/$', remove_student, name='remove_student'),
    url(r'^class_list/class_modify/(\d+)/$', perm_required(['class.can_modify'])(class_edit), name='class_modify'),
    
]
