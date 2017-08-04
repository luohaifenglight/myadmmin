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
from .viewmodel import ScoreEnjoyListDQ, CourseSystemCommand, ScoreEnjoyManageListDQ, score_enjoy_office_choices
from .forms import *
from backend.operation_log.viewmodel import OperationLogCommand

import traceback

t_dir = 'score_enjoy/'
t_module = '选弹曲库'


# ＝＝＝＝＝＝欣赏曲库列表＝＝＝＝＝＝＝＝＝
def score_enjoy_list(request):
    http_content = {
        'title': u' 欣赏曲库列表',
        'list_fields': LIST_FIELDS,
        'searches': {},
        'qry_items': QUERY_TYPE,
    }
    if request.method == 'GET':
        msg = ScoreEnjoyCommand().modify(data=request.GET)
        if msg:
            messages.add_message(request, messages.ERROR, msg[1])
    elif request.method == 'POST':
        print request.method

    return render(request, t_dir + 'score_enjoy_list.html', http_content)


def get_scores(request, score_optional_id):
    scores = []
    score = request.POST.getlist('score', [])
    seq = request.POST.getlist('seq', [])
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


from .viewmodel import ScoreEnjoyCommand


def score_enjoy_modify(request, scoreenjoy_id=None):
    """
    欣赏曲目列表 发布  编辑   添加曲子
    """
    try:

        action = 'add'
        pic = ''
        pic_id = ''
        if request.method == 'POST':
            action = request.POST.get('action', '')
            if action == 'add':
                scmd = ScoreEnjoyCommand()
                changenum = scmd.edit_score(request.POST, request.FILES)

                if changenum:
                    messages.add_message(request, messages.SUCCESS, '修改成功')

                return redirect('/score_enjoy/score_enjoy_list/')

            elif action == 'edit':
                scmd = ScoreEnjoyCommand()
                score_id = request.POST.get('score_id')
                changenum = scmd.edit_score(request.POST, request.FILES)

                if changenum:
                    messages.add_message(request, messages.SUCCESS, '修改成功')

                return redirect('/score_enjoy/score_enjoy_list/')
                # return redirect('/bkp/pic/bkp_pic_modify/?opt=edit&id=' + pic_id)


        elif request.method == 'GET':  # get

            action = request.GET.get('opt', 'add')
            score_id = request.GET.get('id', '')
            score = ''
            if score_id:
                sncmd = ScoreEnjoyCommand()
                score = sncmd.score_get(score_id=score_id)
                # form 中包含目标 用于模态框的校验  因此增加默认属性
                form = ScoreEnjoyForm(score)
            else:
                form = ScoreEnjoyForm()
                action = action

        http_content = {
            'title': u'新增欣赏曲目' if 1 is None else u'欣赏曲目详情',
            'action': action,
            'score_id': score_id if score_id else '',
            'form': form,
            'score': score if score else "",
            'segments': score['segments'] if 'segments' in score else  '',
        }
        return render(request, t_dir + 'score_enjoy_form.html', http_content)
    except Exception, e:
        print traceback.print_exc()


class ScoreEnjoyDTView(DataTablesView):
    need_count = True
    global_fields = [
    ]
    rpc_api = ScoreEnjoyListDQ().process


# ＝＝＝＝＝＝＝欣赏曲库管理＝＝＝＝＝＝＝＝＝


# 欣赏曲库列表
def score_enjoy_manage_list(request):
    http_content = {
        'title': u' 欣赏曲库管理列表',
        'list_fields': SEM_LIST_FIELDS,
        'searches': {},
        'qry_items': SEM_QUERY_TYPE,
    }
    return render(request, t_dir + 'score_enjoy_manage_list.html', http_content)


class ScoreEnjoyManageDTView(DataTablesView):
    need_count = True
    global_fields = [
    ]
    rpc_api = ScoreEnjoyManageListDQ().process


def score_enjoy_manage_modify(request, course_system_id=None):
    """
    add ,modify
    """
    if course_system_id is not None:
        score_enjoys = CourseSystemCommand().course_system_get(course_system_id)
    else:
        score_enjoys = None
    if request.method == 'POST':
        scores = get_scores(request, course_system_id)
        msg = CourseSystemCommand(scores).course_system_edit(course_system_id)
        if msg:
            messages.add_message(request, messages.INFO, u'添加曲子成功')
        else:
            messages.add_message(request, messages.INFO, u'顺序重复')

        OperationLogCommand.operationlog_record(request, t_module, '添加曲子')
        return redirect('score_enjoy:score_enjoy_manage_modify', course_system_id)
    else:
        pass

    http_content = {
        'title': u'欣赏曲库详情页',
        'action': 'modify',
        'scores': score_enjoys,
    }
    return render(request, t_dir + 'score_enjoy_manage_form.html', http_content)


def score_enjoy_office_choices_v(request):
    q = request.GET.get('q', '')

    page = int(request.GET.get('page', 1))
    num = int(request.GET.get('num', 30))
    data = score_enjoy_office_choices(q, 0, page, num)
    return JsonResponse(data, safe=False)
