#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.conf import settings
from .forms import InstitutionForm
from django.db.models import Q
from enumtype import *
from django.contrib import messages
from django.http import Http404
from django.http import HttpResponse, JsonResponse
from utils.baseview import DataTablesView
from .viewmodel import InstitutionDQ, InstitutionCommand, province_choices, \
    city_choices, course_system_choices, get_student_ids, reset_student_password
from backend.accounts.enumtype import LIST_FIELDS as a_list
from backend.accounts.viewmodel import AdminDQ, UserCommand
from .forms import AdminForm
from backend.student.viewmodel import StudentDQ
import traceback
from backend.operation_log.viewmodel import OperationLogCommand

t_dir = 'institution/'


def institution_list(request):
    http_content = {
        'title': u'机构列表',
        'list_fields': LIST_FIELDS,
        'searches': {},
        'qry_items': QUERY_TYPE,
    }
    return render(request, t_dir + 'institution_list.html', http_content)


class InstitutionDTView(DataTablesView):
    need_count = True
    global_fields = [
        'id',
        'type',
    ]
    rpc_api = InstitutionDQ().process


def institution_admin_list(request, institution_id=None):
    http_content = {
        'title': u'机构管理员',
        'list_fields': a_list,
        'searches': {},
        'institution_id': int(institution_id),
    }
    print 'jigou:', institution_id
    return render(request, t_dir + 'admin_list.html', http_content)


class ManagerDTView(DataTablesView):
    need_count = True
    global_fields = [
    ]
    rpc_api = AdminDQ().process

    def post(self, request):
        # parse request data
        # build for query params
        institution_id = request.POST.get('institution_id')
        self.parse_request_data(request.POST or None)
        # call rpc datatable api
        data = AdminDQ(init_q=Q(institution_id=institution_id)).process(**self.options)
        data['draw'] = self.draw
        data['recordsTotal'] = data.get('count', 0)
        data['recordsFiltered'] = data.get('count', 0)
        return self.json_response(data)


def admin_edit(request, institution_id=None, user_id=None):
    """
    add ,modify
    """
    if institution_id is None:
        raise Http404()
    if user_id is not None:
        user = UserCommand.user_get(user_id)
    else:
        user = None
    action = 'create' if user is None else 'modify'
    if request.method == 'POST':
        form = AdminForm(request.POST, initial=user)
        if form.is_valid():
            data = form.cleaned_data
            try:
                    # save data----
                data['institution_id'] = institution_id
                data['type'] = 1
                user_id = UserCommand.user_edit(user_id, data)
                if user_id == -1:
                    form.add_error('mobile', u'手机号已经存在')
                    raise Exception("手机号已经存在")
                if user_id == -2:
                    form.add_error('username', u'用户名已经存在')
                    raise Exception("用户名已经存在")
                messages.add_message(request, messages.INFO, u'管理员保存成功')
                if action == 'create':
                    OperationLogCommand.operationlog_record(request, '机构', '新建管理员')
                else:
                    OperationLogCommand.operationlog_record(request, '机构', '修改管理员')
                if request.POST.get('_new', None):
                    return redirect('institution:admin_create', institution_id)
                return redirect('institution:admin_modify', institution_id, user_id)
            except Exception as e:
                print e
                form.add_error(None, u'手机号或用户名已存在｜保存出错')
    else:
        form = AdminForm(user)
    groups = UserCommand.get_groups(user_id) if user else [{'id': '5', 'text': '机构'}]
    http_content = {
        'title': u'新增机构管理员' if user_id is None else u'机构管理员详情页',
        'action': action,
        'form': form,
        'select_options': groups,
        'readonly_fields':  ['belong_groups', 'department']
    }
    return render(request, t_dir + 'admin_form.html', http_content)


def institution_edit(request, institution_id=None):
        """
        add ,modify
        """
        selected_city_options = []
        course_system_options = []
        province = {}
        if institution_id is not None:
            institution = InstitutionCommand().institution_get(institution_id)
            selected_city_options = [{
                'id': institution.get('city', ''),
                'text': institution.get('city_name', '')
            }]
            course_system_options = InstitutionCommand.get_course(institution_id)
            province = institution.get('province', {})
        else:
            institution = None
        action = 'create' if institution is None else 'modify'
        if request.method == 'POST':
            form = InstitutionForm(request.POST, initial=institution)
            if form.is_valid():
                data = form.cleaned_data
                try:
                    # save data----
                    institution_id = InstitutionCommand(data=data).institution_edit(institution_id)
                    messages.add_message(request, messages.INFO, u'机构保存成功')
                    if action == 'create':
                        OperationLogCommand.operationlog_record(request, '机构', '新建')
                    else:
                        OperationLogCommand.operationlog_record(request, '机构', '修改')
                    if request.POST.get('_new', None):
                        return redirect('institution:institution_create')
                    return redirect('institution:institution_modify', institution_id)
                except Exception as e:
                    traceback.print_exc()
                    form.add_error(None, u'保存出错')
        else:
            form = InstitutionForm(institution)
        print selected_city_options
        print course_system_options
        http_content = {
            'title': u'新增机构列表' if institution_id is None else u'机构列表详情页',
            'action': action,
            'form': form,
            'selected_city_options': selected_city_options,
            'course_system_options': course_system_options,
            'province': province,
            'all_ready_only': institution.get('status', 0) if institution else 0,
        }
        return render(request, t_dir + 'institution_form.html', http_content)


def province_choices_v(request):
    q = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    num = int(request.GET.get('num', 30))
    data = province_choices(q, page, num)
    print data
    return JsonResponse(data, safe=False)


def city_choices_v(request):
    q = request.GET.get('q', '')
    province = request.GET.get('province', None)
    page = int(request.GET.get('page', 1))
    num = int(request.GET.get('num', 30))
    data = city_choices(q, page, num, province)
    print data
    return JsonResponse(data, safe=False)


def course_system_choices_v(request):
    q = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    num = int(request.GET.get('num', 30))
    data = course_system_choices(q, page, num)
    print data
    return JsonResponse(data, safe=False)


def reset_status(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        InstitutionCommand.reset_status(id)
        OperationLogCommand.operationlog_record(request, '机构', '重置状态')
        data = {"status": True}
    return JsonResponse(data, safe=False)


def reset_teacher_status(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        InstitutionCommand.reset_status(id, reset_type=1)
        OperationLogCommand.operationlog_record(request, '机构', '重置教师状态')
        data = {"status": True}
    return JsonResponse(data, safe=False)


def reset_password(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        password = request.POST.get('pwd', '')
        reset_student_password(id, password)
        OperationLogCommand.operationlog_record(request, '机构', '重置体验账号密码')
        data = {"status": True}
    return JsonResponse(data, safe=False)


def student_list(request):
    http_content = {
        'title': u' 体验账号列表',
        'list_fields': STUDENT_LIST_FIELDS,
        'searches': {},
        'qry_items': QUERY_TYPE,
    }
    return render(request, t_dir + 'experience_student.html', http_content)


class StudentDTView(DataTablesView):
    need_count = True
    global_fields = [
    ]

    student_ids = get_student_ids()
    print 'student_ids:%s' % str(student_ids)
    rpc_api = StudentDQ(init_q=Q(is_experience_num=1)).process

    def do_exra(self, request):
        admin_type = request.user.accountuser.type
        if admin_type == 1:
            student_ids = get_student_ids(request.user.accountuser.institution.id)
            self.rpc_api = StudentDQ(init_q=Q(experience_students__institution__id=request.user.accountuser.institution.id )).process
