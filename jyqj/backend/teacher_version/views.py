#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.conf import settings
from .forms import TeacherVersionForm
from django.db.models import Q
from enumtype import *
from django.contrib import messages
from django.http import Http404
from django.http import HttpResponse, JsonResponse
from utils.baseview import DataTablesView
from .viewmodel import TeacherVersionDQ, TeacherVersionCommand
from backend.operation_log.viewmodel import OperationLogCommand

import traceback

t_dir = 'teacherversion/'
t_module = '老师端app版本'


def teacherversion_list(request):
    http_content = {
        'title': u'老师端app列表',
        'list_fields': LIST_FIELDS,
        'searches': {},
        'qry_items': QUERY_TYPE,
    }
    return render(request, t_dir + 'teacherversion_list.html', http_content)


def teacherversion_edit(request, teacherversion_id=None):
    """
    add ,modify
    """
    if teacherversion_id is not None:
        teacherversion = TeacherVersionCommand().teacherversion_get(teacherversion_id)
    else:
        teacherversion = None

    action = 'create' if teacherversion is None else 'modify'
    if request.method == 'POST':
        form = TeacherVersionForm(request.POST, initial=teacherversion)
        if form.is_valid():
            data = form.cleaned_data
            try:
                # save data----
                teacherversion_id = TeacherVersionCommand(data=data).teacherversion_edit(teacherversion_id)
                messages.add_message(request, messages.INFO, u'保存版本成功')
                if action == 'create':
                    OperationLogCommand.operationlog_record(request, t_module, '添加')
                else:
                    OperationLogCommand.operationlog_record(request, t_module, '修改')
                if request.POST.get('_new', None):
                    return redirect('teacherversion:teacherversion_create')
                return redirect('teacherversion:teacherversion_modify', teacherversion_id)
            except Exception as e:
                traceback.print_exc()
                form.add_error(None, u'保存出错')
        else:
            form.add_error(None, u'请上传文件')
    else:
        if teacherversion:
            form = TeacherVersionForm(teacherversion)
        else:
            form = TeacherVersionForm(initial={'package_code': TeacherVersionCommand.get_last_package_code()})
    http_content = {
        'title': u'新增app版本' if teacherversion_id is None else u'app版本详情页',
        'action': action,
        'form': form,
        'all_ready_only': teacherversion['status'] if teacherversion else 0,
    }
    return render(request, t_dir + 'teacherversion_form.html', http_content)


class TeacherVersionDTView(DataTablesView):
    need_count = True
    global_fields = [
        'path_name',
    ]
    rpc_api = TeacherVersionDQ().process


def reset_status(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        TeacherVersionCommand.reset_status(id)
        OperationLogCommand.operationlog_record(request, t_module, '更改状态')
        data = {"status": True}
    return JsonResponse(data, safe=False)
