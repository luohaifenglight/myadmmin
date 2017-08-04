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
from .viewmodel import CourseSystemDQ, CourseSystemCommand
from backend.operation_log.viewmodel import OperationLogCommand

import traceback

t_dir = 'score_optional/'
t_module = '选弹曲库'


def score_optional_list(request):
    http_content = {
        'title': u' 选弹曲库列表',
        'list_fields': LIST_FIELDS,
        'searches': {},
        'qry_items': QUERY_TYPE,
    }
    return render(request, t_dir + 'score_optional_list.html', http_content)


def get_scores(request, score_optional_id):
    scores = []
    score = request.POST.getlist('score', [])
    seq = request.POST.getlist('seq', [])
    print seq
    s_type = request.POST.getlist('type', [])
    for index, seg in enumerate(score):
        seg_dic = {
            'score_id': seg,
            'seq': seq[index],
            'type': s_type[index],
            'course_system_id': score_optional_id,
        }
        scores.append(seg_dic)
    return scores


def score_optional_edit(request, scoreoptional_id=None):
    """
    add ,modify
    """
    if scoreoptional_id is not None:
        score_optional = CourseSystemCommand().course_system_get(scoreoptional_id)
    else:
        score_optional = None
    if request.method == 'POST':
        scores = get_scores(request, scoreoptional_id)
        CourseSystemCommand(scores).course_system_edit(scoreoptional_id)
        messages.add_message(request, messages.INFO, u'添加曲子成功')
        OperationLogCommand.operationlog_record(request, t_module, '添加曲子')
        return redirect('score_optional:score_optional_modify', scoreoptional_id)
    else:
        print 'get'
    http_content = {
        'title':  u'选弹曲库详情页',
        'action': 'modify',
        'scores': score_optional,
    }
    return render(request, t_dir + 'score_optional_form.html', http_content)


class ScoreOptionalDTView(DataTablesView):
    need_count = True
    global_fields = [
    ]
    rpc_api = CourseSystemDQ().process
