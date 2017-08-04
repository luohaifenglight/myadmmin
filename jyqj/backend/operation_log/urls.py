#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from backend.accounts.perms import perm_required
from .views import operationlog_list,  OperationLogDTView
operationlog_urls = [
    url(r'^operationlog_list/$', perm_required(['opreationlog.can_view'])(operationlog_list), name='operationlog_list'),
    url(r'^datatable/$', OperationLogDTView.as_view(), name='datatable'),
    
]
