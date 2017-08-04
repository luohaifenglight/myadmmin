#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from backend.accounts.perms import perm_required
from .views import section_list, unit_list, unit_edit, UnitDTView, reset_status, SectionDTView, section_edit, \
    game_choices, delete_section, set_status, section_copy, unit_copy, choices
unit_urls = [
    url(r'^unit_list/$', perm_required(['unit.can_view'])(unit_list), name='unit_list'),
    url(r'^datatable/$', UnitDTView.as_view(), name='datatable'),
    url(r'^unit_list/unit_create/$', perm_required(['unit.can_create'])(unit_edit), name='unit_create'),
    url(r'^unit_list/unit_modify/(\d+)/$', perm_required(['unit.can_modify'])(unit_edit), name='unit_modify'),
    url(r'^reset_status/$', reset_status, name='reset_status'),
    url(r'^unit_list/section_list/(\d+)/$', section_list, name='section_list'),
    url(r'^section_datatable/$', SectionDTView.as_view(), name='section_datatable'),
    url(r'^unit_list/section_list/section_create/(?P<unit_id>(\d)+)/(?P<type>(\d))/$', section_edit,
        name='section_create'),
    url(r'^unit_list/section_list/section_modify/(?P<unit_id>(\d)+)/(?P<type>(\d))/(?P<section_id>(\d)+)/$',
        section_edit, name='section_modify'),
    url(r'^game_choices/$', game_choices, name='game_choices'),
    url(r'^set_status/$', set_status, name='set_status'),
    url(r'^delete_section/$', delete_section, name='delete_section'),
    url(r'^section_copy/$', section_copy, name='section_copy'),
    url(r'^unit_copy/$', unit_copy, name='unit_copy'),
    url(r'^choices/$', choices, name='choices'),
]
