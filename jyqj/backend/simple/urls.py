#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import simple_list, simple_edit, SimpleDTView
simple_urls = [
    url(r'^simple_list/$', simple_list, name='simple_list'),
    url(r'^datatable/$', SimpleDTView.as_view(), name='datatable'),
    url(r'^simple_list/simple_create/$', simple_edit, name='simple_create'),
    url(r'^simple_list/simple_modify/(\d+)/$', simple_edit, name='simple_modify'),
]
