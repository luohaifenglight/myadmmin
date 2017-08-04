#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from backend.accounts.perms import perm_required
from .views import institution_list, institution_edit, InstitutionDTView, province_choices_v, \
    city_choices_v, course_system_choices_v, ManagerDTView, institution_admin_list, admin_edit, \
    reset_status, reset_teacher_status, reset_password, student_list, StudentDTView
institution_urls = [
    url(r'^institution_list/$', perm_required(['institution.can_view'])(institution_list), name='institution_list'),
    url(r'^expreiment_list/$', perm_required(['expreiment_student.can_view'])(student_list), name='student_list'),
    url(r'^datatable/$', InstitutionDTView.as_view(), name='datatable'),
    url(r'^experience_student/datatable/$', StudentDTView.as_view(), name='student_datatable'),
    url(r'^institution_list/institution_create/$', perm_required(['institution.can_create'])(institution_edit), name='institution_create'),
    url(r'^institution_list/institution_modify/(\d+)/$', perm_required(['institution.can_modify'])(institution_edit), name='institution_modify'),
    url(r'^province_choices/$', province_choices_v, name='province_choices'),
    url(r'^city_choices/$', city_choices_v, name='city_choices'),
    url(r'^course_system_choices/$', course_system_choices_v, name='course_system_choices'),
    url(r'^institution_list/admin_list/(\d+)/$', institution_admin_list, name='admin_list'),
    url(r'^admin_datatable/$', ManagerDTView.as_view(), name='admin_datatable'),
    url(r'^reset_status/$', reset_status, name='reset_status'),
    url(r'^reset_password/$', reset_password, name='reset_password'),
    url(r'^reset_teacher_status/$', reset_teacher_status, name='reset_teacher_status'),
    url(r'^institution_list/admin_list/admin_create/(?P<institution_id>(\d+))/$', admin_edit, name='admin_create'),
    url(r'^institution_list/admin_list/admin_modify/(?P<institution_id>(\d)+)/(?P<user_id>(\d)+)/$', admin_edit, name='admin_modify'),
]
