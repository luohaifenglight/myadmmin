#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.conf import settings
from django.db.models import Q
from enumtype import *
from django.contrib import messages
from django.http import Http404
from django.http import HttpResponse, JsonResponse
from .forms import CourseSystemForm
from utils.baseview import DataTablesView
from .viewmodel import CourseSystemDQ, CourseSystemCommand
from backend.operation_log.viewmodel import OperationLogCommand

import traceback

t_dir = 'course_system/'
t_module = '课程体系'


def course_system_list(request):
    http_content = {
        'title': u'课程体系列表',
        'list_fields': LIST_FIELDS,
        'searches': {},
        'qry_items': QUERY_TYPE,
    }
    return render(request, t_dir + 'course_system_list.html', http_content)


def get_coordinates(request, course_system_id):
    scores = []
    x = request.POST.getlist('x', [])
    y = request.POST.getlist('y', [])
    seq = request.POST.getlist('seq', [])
    if len(seq) != len(set(seq)):
        return -1
    print seq
    for index, seg in enumerate(x):
        seg_dic = {
            'x': seg,
            'y': y[index],
            'seq': seq[index],
            'course_system_id': course_system_id,
        }
        scores.append(seg_dic)
    return scores


def course_system_edit(request, coursesystem_id=None):
    """
    add ,modify
    """
    if coursesystem_id is not None:
        course_system = CourseSystemCommand().course_system_get(coursesystem_id)
    else:
        course_system = None
    action = 'create' if course_system is None else 'modify'
    if request.method == 'POST':
        form = CourseSystemForm(request.POST, initial=course_system)
        if form.is_valid():
            data = form.cleaned_data

            try:
                coordinates = get_coordinates(request, coursesystem_id)
                if coordinates == -1:
                    form.add_error(None, u'顺序重复')
                    raise FloatingPointError

                data['coordinates'] = coordinates
                # save data----
                coursesystem_id = CourseSystemCommand(data=data).course_system_edit(coursesystem_id)
                if coursesystem_id == -2:
                    form.add_error(None, u'名称重复')
                    raise FloatingPointError
                messages.add_message(request, messages.INFO, u'保存课程体系成功')
                if action == 'create':
                    OperationLogCommand.operationlog_record(request, t_module, '添加')
                else:
                    OperationLogCommand.operationlog_record(request, t_module, '修改')
                if request.POST.get('_new', None):
                    return redirect('course_system:course_system_create')
                return redirect('course_system:course_system_modify', coursesystem_id)
            except Exception as e:
                traceback.print_exc()
                form.add_error(None, u'保存出错')
        else:
            form.add_error(None, u'请上传')
    else:
        form = CourseSystemForm(course_system)
    http_content = {
        'title': u'新增课程体系' if coursesystem_id is None else u'课程体系详情页',
        'action': action,
        'form': form,
        'coordinates': course_system['coordinates'] if course_system else [],
    }
    return render(request, t_dir + 'course_system_form.html', http_content)


class CourseSystemDTView(DataTablesView):
    need_count = True
    global_fields = [
    ]
    rpc_api = CourseSystemDQ().process
