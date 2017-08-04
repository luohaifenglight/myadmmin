#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.conf import settings
from django.db.models import Q
from enumtype import *
from django.contrib import messages
from django.http import Http404
from django.http import HttpResponse, JsonResponse
from utils.baseview import DataTablesView
from .viewmodel import StudentDQ, StudentCommand
from backend.operation_log.viewmodel import OperationLogCommand

import traceback

t_dir = 'student/'
t_module = '学员'


def student_list(request):
    http_content = {
        'title': u' 学员列表',
        'list_fields': LIST_FIELDS,
        'searches': {},
        'qry_items': QUERY_TYPE,
    }
    return render(request, t_dir + 'student_list.html', http_content)


def student_edit(request, student_id=None):
    """
    add ,modify
    """
    if student_id is not None:
        studentes = StudentCommand().student_get(student_id)
    else:
        studentes = None
    http_content = {
        'title':  u'学员详情页',
        'action': 'modify',
        'student': studentes,
        'class_record': StudentCommand.get_all_record(student_id)
    }
    return render(request, t_dir + 'student_form.html', http_content)


class StudentDTView(DataTablesView):
    need_count = True
    global_fields = [
    ]
    rpc_api = StudentDQ().process

    def do_exra(self, request):
        admin_type = request.user.accountuser.type
        if admin_type == 1:
            self.rpc_api = StudentDQ(init_q=Q(classes__teacher__institution__id=request.user.accountuser.institution.id)).process


def class_choices(request):
    q = request.GET.get('q', '')
    student_id = request.GET.get('student_id', None)
    page = int(request.GET.get('page', 1))
    num = int(request.GET.get('num', 30))
    institution_id = request.user.accountuser.institution.id
    data = StudentCommand.class_choices(q, page, num, student_id, institution_id)
    print data
    return JsonResponse(data, safe=False)


def class_move(request):
    if request.method == 'POST':
        class_id = request.POST.get('class_id', '')
        student_id = request.POST.get('student_id', '')
        result = StudentCommand.class_move(class_id, student_id)
        if result == -1:
            data = {
                "status": False,
                "message": u"请直接去目标班级添加！",
            }
            return JsonResponse(data, safe=False)
        elif result == -3:
            data = {
                "status": False,
                "message": u"体验学生不能转到正常班级！",
            }
            return JsonResponse(data, safe=False)
        OperationLogCommand.operationlog_record(request, t_module, '转班')
        data = {"status": True}
    return JsonResponse(data, safe=False)
