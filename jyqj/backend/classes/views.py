#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.conf import settings
from django.db.models import Q
from enumtype import *
from django.contrib import messages
from django.http import Http404
from django.http import HttpResponse, JsonResponse
from backend.student.viewmodel import StudentDQ
from utils.baseview import DataTablesView
from .viewmodel import ClassDQ, ClassCommand, course_system_choices, teacher_choices
from .forms import ClassForm
from backend.operation_log.viewmodel import OperationLogCommand

import traceback

t_dir = 'class/'
t_module = '班级'


def class_list(request):
    http_content = {
        'title': u' 班级列表',
        'list_fields': LIST_FIELDS,
        'searches': {},
        'qry_items': QUERY_TYPE,
    }
    return render(request, t_dir + 'class_list.html', http_content)


def class_edit(request, class_id=None):
    """
    add ,modify
    """
    if class_id is not None:
        classes = ClassCommand().class_get(class_id)
    else:
        classes = None
    action = 'create' if classes is None else 'modify'
    if request.method == 'POST':
        form = ClassForm(request.POST, initial=classes)
        if form.is_valid():
            data = form.cleaned_data
            try:
                # save data----
                class_id = ClassCommand(data=data).class_edit(class_id)
                if class_id == -2:
                    form.add_error(None, u'教师课程体系与当前选择不一致')
                    raise
                if class_id == -3:
                    form.add_error(None, u'体验班不能修改课程体系为非体验课程体系')
                    raise
                messages.add_message(request, messages.INFO, u'添加班级成功')
                if action == 'create':
                    OperationLogCommand.operationlog_record(request, t_module, '新建')
                else:
                    OperationLogCommand.operationlog_record(request, t_module, '修改')
                if request.POST.get('_new', None):
                    return redirect('class:class_create')
                return redirect('class:class_modify', class_id)
            except Exception as e:
                traceback.print_exc()
                form.add_error(None, u'保存出错')
    else:
        form = ClassForm(classes)
    http_content = {
        'title': u'新增班级' if class_id is None else u'班级详情详情页',
        'action': action,
        'form': form,
        'classes': classes,
        'course_system_choices': [{'id': classes.get('course_system'), 'text': classes.get('course_system_name')}] if classes else [],
        'teacher_choices': [{'id': classes.get('teacher'), 'text': classes.get('teacher_name')}] if classes else [],
        'all_ready_only': not request.user.accountuser.type,
    }
    print http_content['course_system_choices'], http_content['teacher_choices']
    return render(request, t_dir + 'class_form.html', http_content)


class ClassDTView(DataTablesView):
    need_count = True
    global_fields = [
    ]
    rpc_api = ClassDQ().process

    def do_exra(self, request):
        admin_type = request.user.accountuser.type
        if admin_type == 1:
            self.rpc_api = ClassDQ(init_q=Q(teacher__institution__id=request.user.accountuser.institution.id)).process


def remove_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id', '')
        class_id = request.POST.get('class_id', '')
        if ClassCommand.remove_student(class_id, student_id):
            OperationLogCommand.operationlog_record(request, t_module, '移除学生')
            data = {"status": True}
        else:
            data = {"status": False}
    return JsonResponse(data, safe=False)


def add_student(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile', '')
        class_id = request.POST.get('id', '')
        result_status = ClassCommand.add_student(class_id, mobile, request.user.accountuser.institution.id)
        if result_status > 0:
            OperationLogCommand.operationlog_record(request, t_module, '添加学生')
            data = {"status": True}
        else:
            message = ADD_STUDENT_STATUS.getDesc(result_status)
            data = {"status": False, "message": message}
    return JsonResponse(data, safe=False)


def student_list(request, class_id=None):
    http_content = {
        'title': u'%s 班班级学员列表' % str(class_id),
        'list_fields': STUDENT_LIST_FIELDS,
        'searches': {},
        'qry_items': [],
        'class_id': class_id,
    }
    return render(request, t_dir + 'student_list.html', http_content)


class StudentDTView(DataTablesView):
    need_count = True
    global_fields = [
    ]
    rpc_api = StudentDQ().process

    def post(self, request):
        # parse request data
        # build for query params
        class_id = request.POST.get('class_id')
        print 'class_id:%s' %str(class_id)
        self.parse_request_data(request.POST or None)
        # call rpc datatable api
        data = StudentDQ(init_q=Q(classes__id=class_id)).process(**self.options)
        data['draw'] = self.draw
        data['recordsTotal'] = data.get('count', 0)
        data['recordsFiltered'] = data.get('count', 0)
        return self.json_response(data)


def course_system_choices_v(request):
    q = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    num = int(request.GET.get('num', 30))
    instition_id = request.user.accountuser.institution.id
    data = course_system_choices(q, page, num, instition_id)
    print data
    return JsonResponse(data, safe=False)


def teacher_choices_v(request):
    q = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    num = int(request.GET.get('num', 30))
    instition_id = request.user.accountuser.institution.id
    data = teacher_choices(q, page, num, instition_id)
    print data
    return JsonResponse(data, safe=False)



