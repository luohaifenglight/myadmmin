#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.conf import settings
from .forms import TeacherForm
from django.db.models import Q
from enumtype import *
from django.contrib import messages
from django.http import Http404
from django.http import HttpResponse, JsonResponse
from utils.baseview import DataTablesView
from .viewmodel import TeacherDQ, TeacherCommand
from backend.accounts.enumtype import LIST_FIELDS as a_list
from backend.accounts.viewmodel import AdminDQ, UserCommand
from backend.operation_log.viewmodel import OperationLogCommand

import traceback

t_dir = 'teacher/'
t_module = '教师'

def teacher_list(request):
    http_content = {
        'title': u'教师列表',
        'list_fields': LIST_FIELDS,
        'searches': {},
        'qry_items': QUERY_TYPE,
    }
    return render(request, t_dir + 'teacher_list.html', http_content)


def get_teacher_by_mobile(request):
    mobile = request.GET.get('mobile', '')
    data = {'name': TeacherCommand.get_teacher_by_mobile(mobile).get('name', '')}
    return JsonResponse(data, safe=False)


def teacher_edit(request, teacher_id=None):
    """
    add ,modify
    """
    selected_city_options = []
    course_system_options = []
    province = {}
    if teacher_id is not None:
        teacher = TeacherCommand().teacher_get(teacher_id)
        selected_city_options = [{
            'id': teacher.get('city', ''),
            'text': teacher.get('city_name', '')
        }]
        course_system_options = TeacherCommand.get_course(teacher_id)
        province = teacher.get('province', {})
    else:
        teacher = None
    action = 'create' if teacher is None else 'modify'
    if request.method == 'POST':
        form = TeacherForm(request.POST, initial=teacher)
        if form.is_valid():
            data = form.cleaned_data
            data['institution_id'] = request.user.accountuser.institution.id
            try:
                # save data----
                teacher_id = TeacherCommand(data=data).teacher_edit(teacher_id)
                if teacher_id == -1:
                    messages.add_message(request, messages.ERROR, u'教师不存在')
                    raise FloatingPointError
                if teacher_id == -2:
                    messages.add_message(request, messages.ERROR, u'该老师已被其他机构添加')
                    raise FloatingPointError
                if teacher_id == -3:
                    messages.add_message(request, messages.ERROR, u'超过该机构的老师数量')
                    raise FloatingPointError
                messages.add_message(request, messages.INFO, u'添加教师成功')
                if action == 'create':
                    OperationLogCommand.operationlog_record(request, t_module, '新建')
                else:
                    OperationLogCommand.operationlog_record(request, t_module, '修改')
                if request.POST.get('_new', None):
                    return redirect('teacher:teacher_create')
                return redirect('teacher:teacher_modify', teacher_id)
            except Exception as e:
                traceback.print_exc()
                form.add_error(None, u'保存出错')
    else:
        form = TeacherForm(teacher)
    print selected_city_options
    print course_system_options
    http_content = {
        'title': u'新增教师' if teacher_id is None else u'教师详情页',
        'action': action,
        'form': form,
        'selected_city_options': selected_city_options,
        'course_system_options': course_system_options,
        'province': province,
        'all_ready_only': not request.user.accountuser.type,
    }
    return render(request, t_dir + 'teacher_form.html', http_content)


class TeacherDTView(DataTablesView):
    need_count = True
    global_fields = [
        'id',
        'name',
        'mobile',
    ]
    rpc_api = TeacherDQ().process

    def do_exra(self, request):
        admin_type = request.user.accountuser.type
        if admin_type == 1:
            self.rpc_api = TeacherDQ(init_q=Q(institution_id=request.user.accountuser.institution.id)).process


def course_system_choices_v(request):
    q = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    num = int(request.GET.get('num', 30))
    insti_id = request.user.accountuser.institution.id
    data = TeacherCommand.course_system_choices(q, page, num, insti_id)
    print insti_id, data
    return JsonResponse(data, safe=False)


