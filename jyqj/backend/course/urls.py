#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from backend.accounts.perms import perm_required
from .views import course_list, course_edit, CourseDTView, reset_status, course_copy
course_urls = [
    url(r'^course_list/$', perm_required(['course.can_view'])(course_list), name='course_list'),
    url(r'^datatable/$', CourseDTView.as_view(), name='datatable'),
    url(r'^course_list/course_create/$', perm_required(['course.can_create'])(course_edit), name='course_create'),
    url(r'^course_list/course_modify/(\d+)/$', perm_required(['course.can_modify'])(course_edit), name='course_modify'),
    url(r'^reset_status/$', reset_status, name='reset_status'),
    url(r'^course_copy/$', course_copy, name='course_copy'),
]
