#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from backend.accounts.perms import perm_required
from .views import course_system_list, course_system_edit, CourseSystemDTView
course_system_urls = [
    url(r'^course_system_list/$', course_system_list, name='course_system_list'),
    url(r'^datatable/$', CourseSystemDTView.as_view(), name='datatable'),
    url(r'^course_system_list/course_system_create/$', course_system_edit, name='course_system_create'),
    url(r'^course_system_list/course_system_modify/(\d+)/$', course_system_edit, name='course_system_modify'),
    
]
