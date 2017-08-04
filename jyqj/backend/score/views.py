#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.conf import settings
from .forms import ScoreForm, QnydScoreForm
from django.db.models import Q
from enumtype import *
from django.contrib import messages
from django.http import Http404
from django.http import HttpResponse, JsonResponse
from utils.baseview import DataTablesView
from .viewmodel import ScoreDQ, ScoreCommand, timbre_choices, QnydScoreCommand, \
    music_office_choices, segment_choices as seg_ch, all_choices
from backend.operation_log.viewmodel import OperationLogCommand

import traceback

t_dir = 'score/'
t_module = '曲库'


def score_list(request):
    http_content = {
        'title': u' 曲库列表',
        'list_fields': LIST_FIELDS,
        'searches': {},
        'qry_items': QUERY_TYPE,
    }
    return render(request, t_dir + 'score_list.html', http_content)


def get_segments(request):
    start_time = request.POST.getlist('start_time', [])
    end_time = request.POST.getlist('end_time', [])
    label_info = request.POST.getlist('label_info', [])
    segment_type = request.POST.getlist('segment_type', [])
    segment_id = request.POST.getlist('segment_id', [])
    segments = []
    for index, seg in enumerate(start_time):
        seg_dic = {
            'start': seg,
            'end': end_time[index],
            'label': label_info[index],
            'type': segment_type[index],
            'id': '' if segment_id[index] == 'no' else segment_id[index],
        }
        segments.append(seg_dic)
    return segments


def get_score_images(image_path, image_name, seq):
    images = []
    for index, seg in enumerate(image_path):
        seg_dic = {
            'pic_path': seg,
            'pic_name': image_name[index],
            'seq': seq[index],
        }
        images.append(seg_dic)
    return images


def score_edit(request, score_id=None):
    """
    add ,modify
    """
    if score_id is not None:
        score = ScoreCommand().score_get(score_id)
    else:
        score = None
    action = 'create' if score is None else 'modify'
    is_temp_data = False
    temp_data = {}
    if request.method == 'POST':

        image_path = request.POST.getlist('score_image_path', [])
        image_name = request.POST.getlist('score_image_name', [])
        delete_id = request.POST.get('delete_id', '')
        print 'image_name %s %s' % (image_name, image_path)
        seq = request.POST.getlist('seq', [])
        print str(request.POST)
        form = ScoreForm(request.POST, initial=score)
        if form.is_valid():
            data = form.cleaned_data
            # data['music_type'] = 0
            data['admin_id'] = request.user.accountuser.id
            data['segments'] = get_segments(request)
            data['delete_id'] = delete_id
            data['score_images'] = get_score_images(image_path, image_name, seq)
            try:
                # save data----
                if not data['segments']:
                    form.add_error(None, u'分段不能为空')
                    raise
                if not data['score_images']:
                    form.add_error(None, u'图片不能为空')
                    raise
                score_id = ScoreCommand(data=data).score_edit(score_id)
                if score_id < 0:
                    form.add_error(None, ERROR_MESSAGE[score_id])
                    raise
                messages.add_message(request, messages.INFO, u'添加曲库成功')
                if action == 'create':
                    OperationLogCommand.operationlog_record(request, t_module, '新建独奏曲')
                else:
                    OperationLogCommand.operationlog_record(request, t_module, '修改独奏曲')
                if request.POST.get('_new', None):
                    return redirect('score:score_create')
                return redirect('score:score_modify', score_id)
            except Exception as e:
                traceback.print_exc()
                form.add_error(None, u'保存出错')
                is_temp_data = True
                data = {}
                data['segments'] = get_segments(request)
                data['delete_id'] = delete_id
                data['score_images'] = get_score_images(image_path, image_name, seq)
                for s in data['segments']:
                    if not s['id']:
                        s['id'] = 'no'
                temp_data = {
                    'segments': data['segments'],
                    'score_images': data['score_images'],
                    'delete_id': delete_id,
                }
        else:
            is_temp_data = True
            data = {}
            data['segments'] = get_segments(request)
            data['delete_id'] = delete_id
            data['score_images'] = get_score_images(image_path, image_name, seq)
            for s in data['segments']:
                if not s['id']:
                    s['id'] = 'no'
            temp_data = {
                'segments': data['segments'],
                'score_images': data['score_images'],
                'delete_id': data['delete_id']
            }

    else:
        form = ScoreForm(score)
    http_content = {
        'title': u'新增独奏/合奏曲库' if score_id is None else u'独奏曲库／合奏曲库详情页',
        'action': action,
        'form': form,
        'timbre_options': score['timbres'] if score else [],
        'segments': score['segments'] if score else [],
        'score_images': score['score_images'] if score else [],
        'all_ready_only': score['status'] if score else 0,
    }
    if is_temp_data:
        http_content.update(temp_data)
    return render(request, t_dir + 'score_form.html', http_content)


class ScoreDTView(DataTablesView):
    need_count = True
    global_fields = [
        'name',
    ]
    rpc_api = ScoreDQ().process


def timbre_choices_v(request):
    q = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    num = int(request.GET.get('num', 30))
    data = timbre_choices(q, page, num)
    print data
    return JsonResponse(data, safe=False)

def all_choices_v(request):
    q = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    num = int(request.GET.get('num', 30))
    data = all_choices(q, page, num)
    print data
    return JsonResponse(data, safe=False)

def music_office_choices_v(request):
    q = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    num = int(request.GET.get('num', 30))
    data = music_office_choices(q, 0, page, num)
    print data
    return JsonResponse(data, safe=False)


def hzq_office_choices_v(request):
    q = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    num = int(request.GET.get('num', 30))
    data = music_office_choices(q, 1, page, num)
    print data
    return JsonResponse(data, safe=False)

def qnyd_score_edit(request, score_id=None):
    """
    add ,modify
    """
    if score_id is not None:
        score = QnydScoreCommand().score_get(score_id)
    else:
        score = None
    action = 'create' if score is None else 'modify'
    if request.method == 'POST':
        image_path = request.POST.getlist('score_image_path', [])
        image_name = request.POST.getlist('score_image_name', [])
        print 'image_name %s %s' % (image_name, image_path)
        seq = request.POST.getlist('seq', [])
        print str(request.POST)
        form = QnydScoreForm(request.POST, initial=score)
        if form.is_valid():
            data = form.cleaned_data
            data['music_type'] = 1
            data['admin_id'] = request.user.accountuser.id
            data['score_images'] = get_score_images(image_path, image_name, seq)
            try:
                # save data----
                if not data['score_images']:
                    form.add_error(None, u'图片不能为空')
                    raise
                score_id = QnydScoreCommand(data=data).score_edit(score_id)
                messages.add_message(request, messages.INFO, u'保存合奏曲库成功')
                if action == 'create':
                    OperationLogCommand.operationlog_record(request, t_module, '新建合奏曲')
                else:
                    OperationLogCommand.operationlog_record(request, t_module, '修改合奏曲')
                if request.POST.get('_new', None):
                    return redirect('score:qnyd_score_create')
                return redirect('score:qnyd_score_modify', score_id)
            except Exception as e:
                traceback.print_exc()
                form.add_error(None, u'保存出错')
    else:
        form = QnydScoreForm(score)
    http_content = {
        'title': u'新增合奏曲库' if score_id is None else u'合奏曲库详情页',
        'action': action,
        'form': form,
        'music_office': score['music_office'] if score else[{},{},{}],
        'score_images': score['score_images'] if score else [],
        'all_ready_only': score['status'] if score else 0,
    }
    return render(request, t_dir + 'qnyd_score_form.html', http_content)


def reset_status(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        ScoreCommand.reset_status(id)
        OperationLogCommand.operationlog_record(request, t_module, '重置状态')
        data = {"status": True}
    return JsonResponse(data, safe=False)


def segment_choices(request):
    q = request.GET.get('q', '')
    score = request.GET.get('score', None)
    page = int(request.GET.get('page', 1))
    num = int(request.GET.get('num', 30))
    data = seg_ch(q, page, num, score)
    print data
    return JsonResponse(data, safe=False)


def score_delete(request):
    if request.method == 'POST':
        score_id = request.POST.get('id', '')
        result_status = ScoreCommand.delete_score(score_id)
        if result_status > 0:
            OperationLogCommand.operationlog_record(request, t_module, '删除曲子')
            data = {"status": True}
        else:
            message = u'该曲子有相关连的模块，不能删除'
            data = {"status": False, "message": message}
    return JsonResponse(data, safe=False)


def score_copy(request):
    if request.method == 'POST':
        score_id = request.POST.get('id', '')
        result_status = ScoreCommand.copy_score(score_id)
        if result_status > 0:
            OperationLogCommand.operationlog_record(request, t_module, '复制曲子')
            data = {"status": True}
        else:
            message = u'该曲子有相关连的模块，不能删除'
            data = {"status": False, "message": message}
    return JsonResponse(data, safe=False)