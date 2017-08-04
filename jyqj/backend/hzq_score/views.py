#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.conf import settings
from .forms import  QnydScoreForm
from django.db.models import Q
from enumtype import *
from django.contrib import messages
from django.http import Http404
from django.http import HttpResponse, JsonResponse
from utils.baseview import DataTablesView
from .viewmodel import HZQScoreDQ, QnydScoreCommand
from backend.operation_log.viewmodel import OperationLogCommand

import traceback

t_dir = 'hzqscore/'
t_module = '合奏组合'


def score_list(request):
    http_content = {
        'title': u' 合奏组合列表',
        'list_fields': LIST_FIELDS,
        'searches': {},
        'qry_items': QUERY_TYPE,
    }
    return render(request, t_dir + 'hzq_score_list.html', http_content)


class HZQScoreDTView(DataTablesView):
    need_count = True
    global_fields = [
        'name',
    ]
    rpc_api = HZQScoreDQ().process


def hzq_score_edit(request, score_id=None):
    """
    add ,modify
    """
    if score_id is not None:
        score = QnydScoreCommand().score_get(score_id)
    else:
        score = None
    action = 'create' if score is None else 'modify'
    if request.method == 'POST':
        print str(request.POST)
        form = QnydScoreForm(request.POST, initial=score)
        if form.is_valid():
            data = form.cleaned_data
            try:
                # save data----
                score_id = QnydScoreCommand(data=data).score_edit(score_id)
                if score_id == -2:
                    form.add_error("whole_score", u'已经存在总谱ID的曲子')
                    raise
                messages.add_message(request, messages.INFO, u'保存合奏组合成功')
                if action == 'create':
                    OperationLogCommand.operationlog_record(request, t_module, '新建合奏组合')
                else:
                    OperationLogCommand.operationlog_record(request, t_module, '修改合奏组合')
                if request.POST.get('_new', None):
                    return redirect('hzqscore:qnyd_score_create')
                return redirect('hzqscore:qnyd_score_modify', score_id)
            except Exception as e:
                traceback.print_exc()
                form.add_error(None, u'保存出错')
    else:
        form = QnydScoreForm(score)
    http_content = {
        'title': u'新增合奏组合' if score_id is None else u'合奏组合详情页',
        'action': action,
        'form': form,
        'music_office': score['music_office'] if score else[{},{},{}],
    }
    return render(request, t_dir + 'qnyd_score_form.html', http_content)
