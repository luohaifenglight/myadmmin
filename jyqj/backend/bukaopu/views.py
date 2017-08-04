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

from .viewmodel import *
from .forms import *
from .enumtype import *
import traceback

from rest_framework.decorators import api_view, permission_classes, authentication_classes
import json
from django.views.decorators.csrf import csrf_exempt


t_dir = 'bukaopu/'


@api_view(['POST', 'GET'])
# @permission_classes((AllowAny,))
def bkp_pic_list(request):
    try:
        http_content = {
            'title': u'不靠谱图片',
            'list_fields': LIST_FIELDS,
            'searches': {},
            'qry_items': QUERY_TYPE,
        }
        if request.method == 'GET':
            msg = BKPPicCommand().modify(data=request.GET)
            if msg:
                messages.add_message(request._request, messages.ERROR, msg[1])

            return render(request, t_dir + 'bkp_pic_list.html', http_content)
        elif request.method == 'POST':
            print request.method
    except Exception, e:
        print traceback.print_exc()


@api_view(['POST', 'GET'])
# @permission_classes((AllowAny,))
def bkp_pic_modify(request):
    try:

        action = 'add'
        pic = ''
        pic_id = ''
        if request.method == 'POST':
            form = BKPPicForm(request.POST)
            action = request.POST.get('action', '')

            if form.is_valid():
                if action == 'add':
                    bkpcmd = BKPPicCommand()
                    bkp_pic = bkpcmd.add_pic(request.POST, request.FILES)

                    if bkp_pic:
                        bkpcmd.save_target(bkp_pic, request.POST)
                        messages.add_message(request._request, messages.SUCCESS, '添加成功')
                    return redirect('/bkp/pic/bkp_pic_list/')

                elif action == 'edit':
                    bkpcmd = BKPPicCommand()
                    pic_id = request.POST.get('pic_id')
                    changenum = bkpcmd.edit_pic(request.POST, request.FILES)

                    if changenum:
                        bkpcmd.edit_target(request.POST)
                        messages.add_message(request._request, messages.SUCCESS, '修改成功')

                    return redirect('/bkp/pic/bkp_pic_list/')
                    # return redirect('/bkp/pic/bkp_pic_modify/?opt=edit&id=' + pic_id)
            else:
                print form.errors

        elif request.method == 'GET':  # get

            action = request.GET.get('opt', 'add')
            pic_id = request.GET.get('id', '')
            if pic_id:
                bkpcmd = BKPPicCommand()
                pic = bkpcmd.pic_get(pic_id=pic_id)
                # form 中包含目标 用于模态框的校验  因此增加默认属性
                form = BKPPicForm(pic)
            else:
                form = BKPPicForm()
                action = action

        http_content = {
            'title': u'新增图片' if 1 is None else u'图片详情页面',
            'action': action,
            'pic_id': pic_id if pic_id else '',
            'form': form,
            'pic': pic if pic else "",
            'segments': pic['segments'] if 'segments' in pic else  '',
        }
        return render(request, t_dir + 'bkp_pic_form.html', http_content)
    except Exception, e:
        print traceback.print_exc()


class BKPPicDTView(DataTablesView):
    '''
    DT:DATA TABLE
    DQ:DATA QUERY
    '''
    need_count = True
    global_fields = ['id', 'type']  # 模糊查询相关
    rpc_api = BKPPicDQ().process


# ＝＝＝＝＝＝＝＝＝目标管理＝＝＝＝＝＝＝＝＝＝＝＝

@api_view(['POST', 'GET'])
# @permission_classes((AllowAny,))
def bkp_target_list(request):
    try:
        http_content = {
            'title': u'不靠谱目标',
            'list_fields': TARGET_LIST_FIELDS,
            'searches': {},
            'qry_items': TARGET_QUERY_TYPE,
            'target_list': ''
        }
        if request.method == 'GET':
            target_list = BKPTargetCommand().get_target_list()
            http_content['target_list'] = target_list
            # msg = BKPPicCommand().modify(data=request.GET)
            # if msg: messages.info(request._request, msg[1])
            return render(request, t_dir + 'bkp_target_list.html', http_content)
        elif request.method == 'POST':
            print request.method
    except Exception, e:
        print traceback.print_exc()


@api_view(['POST', 'GET'])
# @permission_classes((AllowAny,))
def bkp_target_modify(request):
    try:
        action = 'add'
        target_id = ''
        if request.method == 'POST':
            action = request.POST.get('action', '')

            bkpcmd = BKPTargetCommand()
            msg, msgbody = bkpcmd.add_target(request.POST, request.FILES)

            if msgbody:
                messages.add_message(request._request, messages.SUCCESS, msgbody)
            return redirect('/bkp/target/bkp_target_list/')

        elif request.method == 'GET':  # get
            action = request.GET.get('opt', 'edit')
            target_id = request.GET.get('id', '')
            if target_id:
                bkpcmd = BKPTargetCommand()
                tgt = bkpcmd.target_by_id(target_id)
                form = BKPTargetForm(tgt)

            else:
                form = BKPTargetForm()
                action = action

        http_content = {
            'title': u'新增目标' if 1 is None else u'目标详情',
            'action': action,
            'target_id': target_id if target_id else '',
            'form': form,
        }

        return render(request, t_dir + 'bkp_target_form.html', http_content)

    except Exception, e:
        print traceback.print_exc()


# ＝＝＝＝＝＝关卡＝＝＝＝＝＝＝＝＝＝＝＝＝

@api_view(['POST', 'GET'])
# @permission_classes((AllowAny,))
def bkp_level_list(request):
    try:
        http_content = {
            'title': u'关卡列表',
            'list_fields': LEVEL_LIST_FIELDS,
            'searches': {},
            'qry_items': LEVEL_QUERY_TYPE,
        }
        if request.method == 'GET':
            msg = BKPLevelCommand().modify(data=request.GET)
            if msg: messages.info(request._request, msg[1])
            return render(request, t_dir + 'bkp_level_list.html', http_content)
        elif request.method == 'POST':
            print request.method
    except Exception, e:
        print traceback.print_exc()


@api_view(['POST', 'GET'])
# @permission_classes((AllowAny,))
@csrf_exempt
def bkp_level_modify(request):
    try:

        action = 'add'
        level = ''
        level_id = ''

        selected_pic_options = BKPLevelCommand.get_all_pics()

        if request.method == 'POST':
            form = BKPLevelForm(request.POST)
            action = request.POST.get('action', '')

            if form.is_valid():
                if action == 'add':
                    bkpcmd = BKPLevelCommand()
                    bkp_pic = bkpcmd.add_level(request.POST, request.FILES)

                    if bkp_pic:
                        bkpcmd.save_round(bkp_pic, request.POST)
                        messages.add_message(request._request, messages.SUCCESS, '添加成功')
                    return redirect('/bkp/level/bkp_level_list/')

                elif action == 'edit':
                    bkpcmd = BKPLevelCommand()
                    level_id = request.POST.get('level_id')
                    changenum = bkpcmd.edit_level(request.POST, request.FILES)

                    bkpcmd.edit_round(request.POST)
                    messages.add_message(request._request, messages.SUCCESS, '修改成功')

                    return redirect('/bkp/level/bkp_level_list/')
            else:
                print form.errors

        elif request.method == 'GET':  # get
            action = request.GET.get('opt', 'add')
            level_id = request.GET.get('id', '')

            if level_id:
                level = BKPLevelCommand().level_get(level_id)
                form = BKPLevelForm(level)
            else:
                form = BKPLevelForm()
                action = action

        http_content = {
            'title': u'新增关卡' if 1 is None else u'关卡详情',
            'action': action,
            'level_id': level_id if level_id else '',
            'form': form,
            'level': level if level else "",  # 关卡信息
            'segments': level['segments'] if 'segments' in level else  '',  # 关卡的轮次信息
            'selected_pic_options': selected_pic_options if selected_pic_options is not None else '',  # 可选的图片列表
        }
        return render(request, t_dir + 'bkp_level_form.html', http_content)
    except Exception, e:
        print traceback.print_exc()


class BKPLevelDTView(DataTablesView):
    '''
    DT:DATA TABLE
    DQ:DATA QUERY
    '''
    need_count = True
    global_fields = ['id', 'type']  # 模糊查询相关
    rpc_api = BKPLevelDQ().process


def pic_choices_v(request):
    q = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    num = int(request.GET.get('num', 30))
    data = [{'1': 'name'}]
    # data = province_choices(q, page, num)
    return JsonResponse(data, safe=False)


def target_choices_v(request):
    pic_id = request.POST.get('pic_id', '')
    res = []
    if pic_id:
        obj = BKPTarget.objects.filter(bkp_pic_id=pic_id)
        if obj.count() > 0:
            res = obj.values('name').distinct()
            for item in res:
                item['num'] = BKPTarget.objects.filter(bkp_pic_id=pic_id, name=item['name']).count()

    data = [{'name': '-------', 'num': 0}]
    data.extend(res)

    return HttpResponse(json.dumps(data), content_type="application/json")


def del_round(request):
    id = request.POST.get('id', '')
    if id:
        res = BKPLevelCommand.del_round(id)

    data = {'success': True, 'id': id}
    return HttpResponse(json.dumps(data), content_type="application/json")
