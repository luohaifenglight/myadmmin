#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.conf import settings
from .forms import VideoForm
from django.db.models import Q
from enumtype import *
from django.contrib import messages
from django.http import Http404
from django.http import HttpResponse, JsonResponse
from utils.baseview import DataTablesView
from .viewmodel import VideoDQ, VideoCommand, video_choices as vc, segment_choices as seg_ch
from backend.operation_log.viewmodel import OperationLogCommand

import traceback

t_dir = 'video/'
t_module = '视频'


def video_list(request):
    http_content = {
        'title': u' 视频列表',
        'list_fields': LIST_FIELDS,
        'searches': {},
        'qry_items': QUERY_TYPE,
    }
    return render(request, t_dir + 'video_list.html', http_content)

def get_segments(start_time, end_time, label_info, segment_id):
    segments = []
    for index, seg in enumerate(start_time):
        seg_dic = {
            'start': seg,
            'end': end_time[index],
            'label': label_info[index],
            'id': '' if segment_id[index] == 'no' else segment_id[index],
        }
        segments.append(seg_dic)
    return segments

def video_edit(request, video_id=None):
    """
    add ,modify
    """
    if video_id is not None:
        video = VideoCommand().video_get(video_id)
    else:
        video = None
    action = 'create' if video is None else 'modify'
    if request.method == 'POST':
        start_time = request.POST.getlist('start_time', [])
        end_time = request.POST.getlist('end_time', [])
        label_info = request.POST.getlist('label_info', [])
        segment_id = request.POST.getlist('segment_id', [])
        delete_id = request.POST.get('delete_id', '')
        print 'start_time:%s' % start_time
        print str(request.POST)
        form = VideoForm(request.POST, initial=video)
        if form.is_valid():
            data = form.cleaned_data
            data['delete_id'] = delete_id
            data['segments'] = get_segments(start_time, end_time, label_info, segment_id)
            try:
                # save data----
                video_id = VideoCommand(data=data).video_edit(video_id)
                messages.add_message(request, messages.INFO, u'保存视频成功')
                if action == 'create':
                    OperationLogCommand.operationlog_record(request, t_module, '添加')
                else:
                    OperationLogCommand.operationlog_record(request, t_module, '修改')
                if request.POST.get('_new', None):
                    return redirect('video:video_create')
                return redirect('video:video_modify', video_id)
            except Exception as e:
                traceback.print_exc()
                form.add_error(None, u'保存出错')
        else:
            form.add_error(None, u'请上传视频')
    else:
        form = VideoForm(video)
    http_content = {
        'title': u'新增视频' if video_id is None else u'视频详情页',
        'action': action,
        'form': form,
        'segments': video['segments'] if video else [],
        'all_ready_only': video['status'] if video else 0,
    }
    return render(request, t_dir + 'video_form.html', http_content)


class VideoDTView(DataTablesView):
    need_count = True
    global_fields = [
        'name',
    ]
    rpc_api = VideoDQ().process


def reset_status(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        VideoCommand.reset_status(id)
        OperationLogCommand.operationlog_record(request, t_module, '更改状态')
        data = {"status": True}
    return JsonResponse(data, safe=False)


def video_choices(request):
    q = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    num = int(request.GET.get('num', 30))
    data = vc(q, page, num)
    print data
    return JsonResponse(data, safe=False)


def segment_choices(request):
    q = request.GET.get('q', '')
    video = request.GET.get('video', None)
    page = int(request.GET.get('page', 1))
    num = int(request.GET.get('num', 30))
    data = seg_ch(q, page, num, video)
    print data
    return JsonResponse(data, safe=False)


def video_delete(request):
    if request.method == 'POST':
        video_id = request.POST.get('id', '')
        result_status = VideoCommand.delete_video(video_id)
        if result_status > 0:
            OperationLogCommand.operationlog_record(request, t_module, '删除视频')
            data = {"status": True}
        else:
            message = u'该视频有相关连的模块，不能删除'
            data = {"status": False, "message": message}
    return JsonResponse(data, safe=False)