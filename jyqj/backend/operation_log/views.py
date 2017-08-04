#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.conf import settings
from enumtype import *
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from utils.baseview import DataTablesView
from .viewmodel import OperationLogDQ, OperationLogCommand

t_dir = 'operationlog/'


def operationlog_list(request):
    http_content = {
        'title': u'操作日志',
        'list_fields': LIST_FIELDS,
        'searches': {},
        'qry_items': QUERY_TYPE,
    }
    return render(request, t_dir + 'operationlog_list.html', http_content)


class OperationLogDTView(DataTablesView):
    need_count = True
    global_fields = [
    ]
    rpc_api = OperationLogDQ().process

