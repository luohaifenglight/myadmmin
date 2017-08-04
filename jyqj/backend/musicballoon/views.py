#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.conf import settings
import traceback

from enumtype import *
import time, os, sys
import hashlib
from django.contrib import messages
from utils.baseview import DataTablesView

from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import BalloonSubLevel, BalloonLevel, BalloonSubLevelOctave
from .forms import SublevelInfo
from django.conf import settings
from .viewmodel import *

t_dir = 'musicballoon/'


@api_view(['POST', 'GET'])
@permission_classes((AllowAny,))
def level_manager(request):
    """
    音乐气球－－关卡管理
    ---
    response_serializer: music_balloon.common.serializers.getsyscodeResponse
    """

    try:

        level_list = BalloonLevel.objects.all()
        res = []
        for item in level_list:
            tmp = {}
            tmp['name'] = item.name
            tmp['type'] = item.type
            tmp['sublevel_sum'] = BalloonSubLevel.objects.filter(level_id=item.id).count()
            tmp['seq'] = item.seq
            tmp['level_id'] = item.id
            res.append(tmp)

        http_content = {
            'title': u'音乐气球-关卡管理',
            'list_fields': LIST_FIELDS,
            'searches': {},
            'qry_items': QUERY_TYPE,
            'col': '',
            'leveldata': res,

        }

        if request.method == 'GET':

            return render(request, 'musicballoon/level_manager.html', http_content)
        elif request.method == 'POST':

            col = [{'orderable': False, 'data': 'seq', 'name': 'seq'},
                   {'orderable': False, 'data': 'name', 'name': 'name'},
                   {'orderable': False, 'data': 'sublevel_sum', 'name': 'sublevel_sum'},
                   {'orderable': False, 'data': 'operate', 'name': 'operate'}, ]

            return res
    except Exception, e:
        print 'level_manager error', traceback.print_exc()


@api_view(['POST', 'GET'])
@permission_classes((AllowAny,))
def level_edit(request):
    """
    音乐气球－－关卡管理
    ---
    response_serializer: music_balloon.common.serializers.getsyscodeResponse
    """

    try:
        if request.method == 'GET':
            balloon_cmd = BalloonLevelCommand()
            msg = balloon_cmd.modify(data=request.GET)
            if msg:
                messages.add_message(request._request, messages.ERROR, msg[1])
            res = balloon_cmd.get_all_sublevel(request.GET.get('lid', ''))
            http_content = {
                'title': u'音乐气球-小关管理',
                'list_fields': LIST_FIELDS,
                'searches': {},
                'qry_items': QUERY_TYPE,
                'col': '',
                'sublevel': res,
                'level_id': request.GET.get('lid')
            }
            return render(request, 'musicballoon/level_edit.html', http_content)
        elif request.method == 'POST':
            pass
    except Exception, e:
        print 'level_manager error', traceback.print_exc()


@csrf_exempt
def sublevel_edit(request):
    """
    音乐气球－－小关配置
    """
    try:
        if request.method == 'GET':
            lid = request.GET.get('lid', 1)
            id = request.GET.get('id', 1)

            # 初始化
            tmp = {}
            oct_map = {}

            sublevel_info = BalloonSubLevel.objects.get(id=id)
            octave = BalloonSubLevelOctave.objects.filter(sub_level_id=id).all()
            # todo 包含四个方式配置

            for item in octave:
                octtype = '_'.join([str(x) for x in ['up' if item.keyboard[0] == '1' else 'down', item.octave_type]])
                oct = {}
                for k in sublevel_octave:
                    oct[k] = getattr(item, k, '')
                    if oct[k] is not None and oct[k] == 0:
                        oct[k] = ''
                oct_map[octtype] = oct

            for k in sublevel_key:
                tmp[k] = getattr(sublevel_info, k, '')

            tmp['oct'] = oct_map
            http_content = {
                'title': u'音乐气球-小关配置',
                'list_fields': LIST_FIELDS,
                'searches': {},
                'qry_items': QUERY_TYPE,
                'sublevel': tmp,
                'level_id': lid
            }

            return render(request, 'musicballoon/sublevel_edit.html', http_content)
        elif request.method == 'POST':

            try:
                msg, msgbody = BalloonLevelCommand()._sublevel_edit(request.POST, request.FILES, 'edit')
                messages.add_message(request, messages.WARNING, msgbody)

            except Exception, e:
                print 'sublevel edit', e

            path = request.get_full_path()
            id = request.POST.get('id')
            lid = request.POST.get('level_id')

            return redirect('/musicballoon/level_manager/sublevel_edit/?lid=' + lid + '&id=' + id + '&opt=edit')

    except Exception, e:
        print 'sublevel_edit error', traceback.print_exc()


@csrf_exempt
def sublevel_add(request):
    '''
    :get http://0.0.0.0:9000/musicballoon/level_manager/sublevel_edit/?lid=1&opt=add
    :param request:
    :return:
    '''
    try:
        if request.method == 'GET':
            lid = request.GET.get('lid')  # todo 校验
            opt = request.GET.get('opt')

            http_content = {
                'title': u'音乐气球-小关配置',
                'list_fields': LIST_FIELDS,
                'searches': {},
                'qry_items': QUERY_TYPE,
                'sublevel': '',
                'level_id': lid
            }
            return render(request, 'musicballoon/sublevel_add.html', http_content)
        elif request.method == 'POST':

            msg, msgbody = BalloonLevelCommand()._sublevel_edit(request.POST, request.FILES, 'add')
            messages.add_message(request, messages.INFO, msgbody)

        return redirect('/musicballoon/level_manager/edit/?lid=' + request.POST.get('level_id'))

    except Exception, e:
        print traceback.print_exc()


class LevelManagerDTView(DataTablesView):
    need_count = True
    global_fields = [
        'id',
        'type',
    ]
    rpc_api = BalloonLevelDQ().process


@api_view(['POST', 'GET'])
@permission_classes((AllowAny,))
def level_manager2(request):
    """
    音乐气球－－关卡管理
    ---
    response_serializer: music_balloon.common.serializers.getsyscodeResponse
    """

    if request.method == 'GET':

        http_content = {
            'title': u'机构列表',
            'list_fields': LIST_FIELDS,
            'searches': {},
            'qry_items': QUERY_TYPE,
        }
        print t_dir + 'institution_list.html'

        return render(request, t_dir + 'institution_list.html', {'http_content': http_content})
    else:

        need_count = True
        global_fields = [
            'id',
            'type',
        ]
        rpc_api = BalloonLevelDQ().process
