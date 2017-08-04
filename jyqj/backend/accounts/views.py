#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.shortcuts import render, redirect

from django.conf import settings
from django.contrib import messages
from utils.baseview import DataTablesView
from django.db.models import Q
from .forms import RoleForm, AdminForm, PasswordForm
from django.http import HttpResponse, JsonResponse
from .viewmodel import AdminDQ, BackendGroupDQ, BackendGroupCommand, all_permission,\
    permission_choices as pc, UserCommand
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login as ll, logout as lo
from .enumtype import LIST_FIELDS, QUERY_TYPE, ROLE_LIST_FIELDS, ROLE_QUERY_TYPE, ADMIN_DEPARTMENT, ADMIN_TYPE
from .perms import has_perms
import hashlib
from backend.operation_log.viewmodel import OperationLogCommand

t_dir = 'accounts/'



def index(request):
    http_content = {
        'title': u'首页',
    }
    print 'GET:', request.GET
    return render(request, t_dir + 'index.html', http_content)


def login(request):
    http_content = {
        'title': u'登录',
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        m = hashlib.md5()
        m.update(username.strip())
        _m = m.hexdigest()
        if not user:
            user, _a = UserCommand.get_user_by_mobile(username.strip())
            con1 = check_password(password, user.password) and hasattr(user, 'accountuser')
            con2 = check_password(password, user.password) and user.username == _m
            if not (con1 or con2):
                user = None
            if con2:
                user = _a

        if user is not None and not user.accountuser.status:
            next_url = request.GET.get('next', '/')
            print request.GET
            try:
                ll(request, user)
            except:
                print 'value_error'
            request.session.set_expiry(3600)
            print next_url
            resp = redirect(next_url)
            return resp
            # 转到成功页面
        else:
            err_msg = u'用户名或密码错误或者此账号被冻结'
            http_content = {
                'title': u'登录',
                'err_msg': err_msg,
            }
    return render(request, t_dir + 'login.html', http_content)



def logout(request):
    try:
        lo(request)
    except:
        pass
    resp = redirect('accounts:login')  # login url
    return resp



def manager(request):
    http_content = {
        'title': u'管理员',
        'list_fields': LIST_FIELDS,
        'searches': {},
        'srch_opts': {
            'ADMIN_DEPARTMENT': ADMIN_DEPARTMENT,
        },
        'qry_items': QUERY_TYPE,
    }
    return render(request, t_dir + 'admin_list.html', http_content)



def role(request):
    http_content = {
        'title': u'角色',
        'list_fields': ROLE_LIST_FIELDS,
        'searches': {},
        'qry_items': ROLE_QUERY_TYPE,
    }
    return render(request, t_dir + 'role_list.html', http_content)


class ManagerDTView(DataTablesView):
    need_count = True
    global_fields = [
        'id',
        'mobile',
    ]
    rpc_api = AdminDQ(init_q=Q(user__is_superuser=0)).process


class RoleDTView(DataTablesView):
    need_count = True
    global_fields = [
        'name',
    ]
    rpc_api = BackendGroupDQ().process


def permission_choices(request):
    q = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    num = int(request.GET.get('num', 30))
    data = pc(q, page, num)
    print data
    return JsonResponse(data, safe=False)


def group_choices(request):
    q = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    num = int(request.GET.get('num', 30))
    data = UserCommand.groups_choices(q, page, num)
    print data
    return JsonResponse(data, safe=False)


def role_edit(request, role_id=None):
    """
    add ,modify
    """
    if role_id is not None:
        role = BackendGroupCommand().backendgroup_get(role_id)
    else:
        role = None
    action = 'create' if role is None else 'modify'
    if request.method == 'POST':
        form = RoleForm(request.POST, initial=role)
        if form.is_valid():
            data = form.cleaned_data
            try:
                # save data----
                role_id = BackendGroupCommand(data=data).backendgroup_edit(role_id)
                messages.add_message(request, messages.INFO, u'role保存成功')
                if request.POST.get('_new', None):
                    return redirect('accounts:role_create')
                if action == 'create':
                    OperationLogCommand.operationlog_record(request, '角色', '新建')
                else:
                    OperationLogCommand.operationlog_record(request, '角色', '修改')
                return redirect('accounts:role_modify', role_id)
            except Exception as e:
                 print e
                 form.add_error(None, u'保存出错')
    else:
        form = RoleForm(role)
    permission = all_permission(role.get('permissions', '')) if role else []
    http_content = {
        'title': u'新增角色' if role_id is None else u'角色详情页',
        'action': action,
        'form': form,
        'select_options': permission,
    }
    return render(request, t_dir + 'role_form.html', http_content)


def admin_edit(request, user_id=None):
    """
    add ,modify
    """
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
                user_id = UserCommand.user_edit(user_id, data)
                if user_id == -1:
                    form.add_error('mobile', u'手机号已经存在')
                    raise Exception("手机号已经存在")
                if user_id == -2:
                    form.add_error('username', u'用户名已经存在')
                    raise Exception("用户名已经存在")
                messages.add_message(request, messages.INFO, u'管理员保存成功')
                if action == 'create':
                    OperationLogCommand.operationlog_record(request, '管理员', '新建')
                else:
                    OperationLogCommand.operationlog_record(request, '管理员', '修改')
                if request.POST.get('_new', None):
                    return redirect('accounts:admin_create')
                return redirect('accounts:admin_modify', user_id)
            except Exception as e:
                print e
                form.add_error(None, u'手机号或用户名已存在｜保存出错')
        else:
            form.add_error(None, u'保存出错')
    else:
        form = AdminForm(user)
    groups = UserCommand.get_groups(user_id) if user else []
    print form.declared_fields
    print groups
    http_content = {
        'title': u'新增管理员' if user_id is None else u'管理员详情页',
        'action': action,
        'form': form,
        'select_options': groups,
    }
    return render(request, t_dir + 'admin_form.html', http_content)


def password_edit(request):
    if request.method == 'POST':

        form = PasswordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                result = UserCommand.update_password(request.user, data['old_password'], data['new_password'])
                if result:
                    messages.add_message(request, messages.INFO, '保存成功')
                    OperationLogCommand.operationlog_record(request, '用户', '修改密码')
                    next_url = request.GET.get('next', '/')
                    resp = redirect(next_url)
                    return resp
                else:
                    form.add_error(None, u'验证出错')
            except:
                form.add_error(None, u'保存出错')
    else:
        form = PasswordForm()
    http_content = {
        'title': u'修改密码',
        'form': form,
    }
    return render(request, t_dir + 'alert_password.html', http_content)


def reset_password(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        password = request.POST.get('pwd', '')
        UserCommand.reset_password(id, password)
        OperationLogCommand.operationlog_record(request, '管理员', '重置密码')
        data = {"status": True}
    return JsonResponse(data, safe=False)


def reset_status(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        UserCommand.reset_status(id)
        OperationLogCommand.operationlog_record(request, '管理员', '重置状态')
        data = {"status": True}
    return JsonResponse(data, safe=False)


def reset_role_status(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        BackendGroupCommand.reset_status(id)
        OperationLogCommand.operationlog_record(request, '角色', '重置状态')
        data = {"status": True}
    return JsonResponse(data, safe=False)

