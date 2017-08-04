#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url

#
# institution_urls = [
#     url(r'^institution_list/$', institution_list, name='institution_list'),
#     url(r'^datatable/$', InstitutionDTView.as_view(), name='datatable'),
#     url(r'^institution_list/institution_create/$', institution_edit, name='institution_create'),
#     url(r'^institution_list/institution_modify/(\d+)/$', institution_edit, name='institution_modify'),
#     url(r'^province_choices/$', province_choices_v, name='province_choices'),
#     url(r'^city_choices/$', city_choices_v, name='city_choices'),
#     url(r'^course_system_choices/$', course_system_choices_v, name='course_system_choices'),
#     url(r'^institution_list/admin_list/(\d+)/$', institution_admin_list, name='admin_list'),
#     url(r'^admin_datatable/$', ManagerDTView.as_view(), name='admin_datatable'),
#     url(r'^reset_status/$', reset_status, name='reset_status'),
#     url(r'^reset_teacher_status/$', reset_teacher_status, name='reset_teacher_status'),
#     url(r'^institution_list/admin_list/admin_create/(?P<institution_id>\d)/$', admin_edit, name='admin_create'),
#     url(r'^institution_list/admin_list/admin_modify/(?P<institution_id>(\d)+)/(?P<user_id>(\d)+)/$', admin_edit, name='admin_modify'),
# ]

from .views import bkp_pic_list, BKPPicDTView, bkp_pic_modify, bkp_target_list, bkp_target_modify, bkp_level_list, \
    bkp_level_modify, BKPLevelDTView,pic_choices_v,target_choices_v,del_round

bkp_urls = [
    url(r'^pic/bkp_pic_list/$', bkp_pic_list, name='bkp_pic_list'),
    url(r'^pic/bkp_pic_modify/$', bkp_pic_modify, name='bkp_pic_list'),
    url(r'^pic/datatable/$', BKPPicDTView.as_view(), name='datatable'),

    url(r'^target/bkp_target_list/$', bkp_target_list, name='bkp_target_list'),
    url(r'^target/bkp_target_modify/$', bkp_target_modify, name='bkp_target_modify'),

    url(r'^level/bkp_level_list/$', bkp_level_list, name='bkp_level_list'),
    url(r'^level/bkp_level_modify/$', bkp_level_modify, name='bkp_level_modify'),
    url(r'^level/datatable/$', BKPLevelDTView.as_view(), name='datatable'),

    url(r'^level/pic_choices/$', pic_choices_v, name='pic_choices'),
    url(r'^level/target_choices/$', target_choices_v, name='target_choices'),
    url(r'^level/del_round/$', del_round, name='del_round'),

    # url(r'^institution_list/institution_create/$', institution_edit, name='institution_create'),
    # url(r'^institution_list/institution_modify/(\d+)/$', institution_edit, name='institution_modify'),
    # url(r'^province_choices/$', province_choices_v, name='province_choices'),
    # url(r'^city_choices/$', city_choices_v, name='city_choices'),
    # url(r'^course_system_choices/$', course_system_choices_v, name='course_system_choices'),
    # url(r'^institution_list/admin_list/(\d+)/$', institution_admin_list, name='admin_list'),
    # url(r'^admin_datatable/$', ManagerDTView.as_view(), name='admin_datatable'),
    # url(r'^reset_status/$', reset_status, name='reset_status'),
    # url(r'^reset_teacher_status/$', reset_teacher_status, name='reset_teacher_status'),
    # url(r'^institution_list/admin_list/admin_create/(?P<institution_id>\d)/$', admin_edit, name='admin_create'),
    # url(r'^institution_list/admin_list/admin_modify/(?P<institution_id>(\d)+)/(?P<user_id>(\d)+)/$', admin_edit, name='admin_modify'),
]
