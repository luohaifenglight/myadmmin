#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.conf import settings
from .forms import UnitForm, SECTION_TYPE_FORM
from django.db.models import Q
from enumtype import *
from django.contrib import messages
from django.http import Http404
from django.http import HttpResponse, JsonResponse
from utils.baseview import DataTablesView
from .viewmodel import UnitDQ, UnitCommand, UnitSectionDQ, SectionCommand, game_choices as game_ch
from backend.operation_log.viewmodel import OperationLogCommand

import traceback

t_dir = 'unit/'
t_module = '单元'


def unit_list(request):
    http_content = {
        'title': u' 单元列表',
        'list_fields': LIST_FIELDS,
        'searches': {},
        'qry_items': QUERY_TYPE,
    }
    return render(request, t_dir + 'unit_list.html', http_content)


def section_list(request, unit_id=None):
    http_content = {
        'title': u'{}单元--环节列表'.format(unit_id),
        'list_fields': SECTION_LIST_FIELDS,
        'searches': {},
        'qry_items': [],
        'unit_id': unit_id,
    }
    return render(request, t_dir + 'section_list.html', http_content)


def unit_edit(request, unit_id=None):
    """
    add ,modify
    """
    if unit_id is not None:
        unit = UnitCommand().unit_get(unit_id)
    else:
        unit = None
    action = 'create' if unit is None else 'modify'
    if request.method == 'POST':
        form = UnitForm(request.POST, initial=unit)
        if form.is_valid():
            try:
                # save data----
                data = form.cleaned_data
                unit_id = UnitCommand(data=data).unit_edit(unit_id)
                messages.add_message(request, messages.INFO, u'保存单元成功')
                if action == 'create':
                    OperationLogCommand.operationlog_record(request, t_module, '添加')
                else:
                    OperationLogCommand.operationlog_record(request, t_module, '修改')
                if request.POST.get('_new', None):
                    return redirect('unit:unit_create')
                return redirect('unit:unit_modify', unit_id)
            except Exception as e:
                traceback.print_exc()
                form.add_error(None, u'保存出错')
        else:
            form.add_error(None, u'error')
    else:
        form = UnitForm(unit)
    http_content = {
        'title': u'新增单元' if unit_id is None else u'单元详情页',
        'action': action,
        'form': form,
        'all_ready_only': unit['status'] if unit else 0,
    }
    return render(request, t_dir + 'unit_form.html', http_content)


class UnitDTView(DataTablesView):
    need_count = True
    global_fields = [
        'name',
    ]
    rpc_api = UnitDQ().process


class SectionDTView(DataTablesView):
    need_count = True
    global_fields = [
    ]
    rpc_api = UnitSectionDQ().process

    def do_exra(self, request):
        unit_id = request.POST.get('unit_id')

        self.rpc_api = UnitSectionDQ(init_q=Q(unit_id=unit_id)).process


def get_scores(request):
    scores = []
    score = request.POST.getlist('score', [])
    keyboard = request.POST.getlist('keyboard', [])
    start_num = request.POST.getlist('star_num', [])
    times = request.POST.getlist('times', [])
    tempos = request.POST.getlist('tempo', [])
    print start_num
    for index, seg in enumerate(score):
        seg_dic = {
            'score_id': seg,
            'keyboard': keyboard[index],
            'star_num': start_num[index],
            'times': times[index],
            'tempo': tempos[index],
        }
        scores.append(seg_dic)
    return scores


def get_score_enjoys(request):
    scores = []
    score = request.POST.getlist('score_enjoy', [])
    for index, seg in enumerate(score):
        seg_dic = {
            'score_enjoy_id': seg,
        }
        scores.append(seg_dic)
    return scores


def section_edit(request, unit_id=None, type=0, section_id=None):
    """
    add ,modify
    """
    if unit_id is None:
        raise Http404()
    if section_id is not None:
        section = SectionCommand().section_get(section_id, type)
    else:
        section = None

    section_form = SECTION_TYPE_FORM[int(type)]
    action = 'create' if section is None else 'modify'
    if request.method == 'POST':
        form = section_form(request.POST, initial=section)

        if form.is_valid():
            data = form.cleaned_data
            try:
                    # save data----
                if int(type) == 4:
                    data['scores'] = get_scores(request)
                    data['score_enjoys'] = get_score_enjoys(request)
                section_id = SectionCommand(data).section_edit(unit_id, type, section_id)
                messages.add_message(request, messages.INFO, u'{}-环节保存成功'.format(SECTION_TYPE.getDesc(int(type))))
                if action == 'create':
                    OperationLogCommand.operationlog_record(request, t_module,
                                                            u'新建环节-{}'.format(SECTION_TYPE.getDesc(int(type))))
                else:
                    OperationLogCommand.operationlog_record(request, t_module,
                                                            u'修改环节-{}'.format(SECTION_TYPE.getDesc(int(type))))
                if request.POST.get('_new', None):
                    return redirect('unit:section_create', unit_id, type)
                return redirect('unit:section_list', unit_id)
            except Exception as e:
                print traceback.print_exc()
                form.add_error(None, u'保存出错')
    else:
        form = section_form(section)
    template_form = SECTION_TYPE_TEMPLATE[int(type)]
    #print section['video_segment_options']
    http_content = {
        'title': u'新增环节-{}'.format(SECTION_TYPE.getDesc(int(type))) if section_id is None else u'修改环节-{}'.format(SECTION_TYPE.getDesc(int(type))),
        'action': action,
        'form': form,
        'select_video_options': section['video_options'] if section else [],
        'select_video_segment_options': section['video_segment_options'] if section else [],
        'select_score_options': section['score_options'] if section else [],
        'select_score_segment_options': section['score_segment_options'] if section else [],
        'select_game_options': section['game_options'] if section else [],
        'scores': section['scores'] if section else [],
        'score_enjoys': section['score_enjoys'] if section else [],
    }
    return render(request, t_dir + template_form, http_content)


def reset_status(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        if UnitCommand.reset_status(id):
            OperationLogCommand.operationlog_record(request, t_module, '更改状态')
            data = {"status": True}
        else:
            data = {"status": False}
    return JsonResponse(data, safe=False)


def game_choices(request):
    q = request.GET.get('q', '')
    score = request.GET.get('type', None)
    page = int(request.GET.get('page', 1))
    num = int(request.GET.get('num', 30))
    data = game_ch(q, page, num, score)
    print data
    return JsonResponse(data, safe=False)


def set_status(request):
    if request.method == 'POST':
        seq = request.POST.get('seq', '')
        SectionCommand.reset_seq(seq)
        OperationLogCommand.operationlog_record(request, t_module, '更改顺序')
        data = {"status": True}
    return JsonResponse(data, safe=False)


def delete_section(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        SectionCommand.delete_section(id)
        OperationLogCommand.operationlog_record(request, t_module, '删除环节')
        data = {"status": True}
    return JsonResponse(data, safe=False)


def section_copy(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        SectionCommand.copy(id)
        OperationLogCommand.operationlog_record(request, t_module, '复制环节')
        data = {"status": True}
    return JsonResponse(data, safe=False)


def unit_copy(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        UnitCommand.copy(id)
        OperationLogCommand.operationlog_record(request, t_module, '复制单元')
        data = {"status": True}
    return JsonResponse(data, safe=False)


def choices(request):
    q = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    num = int(request.GET.get('num', 30))
    data = UnitCommand.unit_choices(q, page, num)
    print data
    return JsonResponse(data, safe=False)
