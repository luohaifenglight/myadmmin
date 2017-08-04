#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.conf import settings
from .forms import CourseForm
from django.db.models import Q
from enumtype import *
from django.contrib import messages
from django.http import Http404
from django.http import HttpResponse, JsonResponse
from utils.baseview import DataTablesView
from .viewmodel import CourseDQ, CourseCommand
from backend.operation_log.viewmodel import OperationLogCommand

import traceback

t_dir = 'course/'
t_module = '课程'


def course_list(request):
    http_content = {
        'title': u' 课程列表',
        'list_fields': LIST_FIELDS,
        'searches': {},
        'qry_items': QUERY_TYPE,
    }
    return render(request, t_dir + 'course_list.html', http_content)


def get_units(request):
    units = []
    unit_ids = request.POST.getlist('unit', [])
    seq = request.POST.getlist('seq_u', [])
    print seq
    for index, seg in enumerate(unit_ids):
        seg_dic = {
            'unit_id': seg,
            'seq': seq[index],
        }
        units.append(seg_dic)
    return units


def course_edit(request, course_id=None):
    """
    add ,modify
    """
    if course_id is not None:
        course = CourseCommand().course_get(course_id)
    else:
        course = None
    action = 'create' if course is None else 'modify'
    if request.method == 'POST':
        form = CourseForm(request.POST, initial=course)
        if form.is_valid():
            data = form.cleaned_data
            data['units'] = get_units(request)
            try:
                # save data----
                course_id = CourseCommand(data=data).course_edit(course_id)
                if course_id == -2:
                    form.add_error('name', u'名称重复')
                elif course_id == -3:
                    form.add_error('seq', u'顺序重复')
                elif course_id == -1:
                    form.add_error(None, u'保存出错')
                else:
                    messages.add_message(request, messages.INFO, u'保存课程成功')
                    if action == 'create':
                        OperationLogCommand.operationlog_record(request, t_module, '添加')
                    else:
                        OperationLogCommand.operationlog_record(request, t_module, '修改')
                    if request.POST.get('_new', None):
                        return redirect('course:course_create')
                    return redirect('course:course_modify', course_id)
            except Exception as e:
                traceback.print_exc()
                form.add_error(None, u'保存出错')
        else:
            form.add_error(None, u'保存出错')
    else:
        form = CourseForm(course)
    http_content = {
        'title': u'新增课程' if course_id is None else u'课程详情页',
        'action': action,
        'form': form,
        'units': course['course_unit'] if course else [],
        'course_system_options': course['course_system'] if course else [],
        'all_ready_only': course['status'] if course else 0,
    }
    return render(request, t_dir + 'course_form.html', http_content)


class CourseDTView(DataTablesView):
    need_count = True
    global_fields = [
        'name',
    ]
    rpc_api = CourseDQ().process


def course_copy(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        CourseCommand.copy(id)
        OperationLogCommand.operationlog_record(request, t_module, '复制课程')
        data = {"status": True}
    return JsonResponse(data, safe=False)


def reset_status(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        if CourseCommand.reset_status(id):
            OperationLogCommand.operationlog_record(request, t_module, '更改状态')
            data = {"status": True}
        else:
            data = {"status": False}
    return JsonResponse(data, safe=False)
