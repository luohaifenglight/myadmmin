#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from perms import perm_required
from .views import login, index, logout, ManagerDTView, manager, \
    role, RoleDTView, role_edit, permission_choices, group_choices, \
    admin_edit, password_edit, reset_password, reset_status, reset_role_status
account_urls = [
    url(r'^login/$', login, name='login'),
    url(r'^index/$', index, name='index'),
    url(r'^change_password/$', password_edit, name='password'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^admin_datatable/$', ManagerDTView.as_view(), name='admin_databale'),
    url(r'^admin/$', perm_required(['accounts.can_view'])(manager), name='admin'),
    url(r'^role_datatable/$', RoleDTView.as_view(), name='role_databale'),
    url(r'^role/$', perm_required(['role.can_view'])(role), name='role'),
    url(r'^role/role_create/$', perm_required(['role.can_create'])(role_edit), name='role_create'),
    url(r'^role/role_modify/(\d+)/$', perm_required(['role.can_modify'])(role_edit), name='role_modify'),
    url(r'^role/permission_choices/$', permission_choices, name='permission_choices'),
    url(r'^admin/group_choices/$', group_choices, name='group_choices'),
    url(r'^admin/reset_password/$', reset_password, name='reset_password'),
    url(r'^admin/reset_status/$', reset_status, name='reset_status'),
    url(r'^role/reset_status/$', reset_role_status, name='reset_role_status'),
    url(r'^admin/admin_create/$', perm_required(['accounts.can_create'])(admin_edit), name='admin_create'),
    url(r'^admin/admin_modify/(\d+)/$', perm_required(['accounts.can_modify'])(admin_edit), name='admin_modify'),
]
