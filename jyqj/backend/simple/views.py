#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.conf import settings
from .forms import SimpleForm
from enumtype import *
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from utils.baseview import DataTablesView
from .viewmodel import SimpleDQ, SimpleCommand

t_dir = 'simple/'


def simple_list(request):
    http_content = {
        'title': u'example',
        'list_fields': LIST_FIELDS,
        'searches': {},
        'qry_items': QUERY_TYPE,
    }
    return render(request, t_dir + 'simple_list.html', http_content)


class SimpleDTView(DataTablesView):
    need_count = True
    global_fields = [
        'f1',
        'f2',
    ]
    rpc_api = SimpleDQ().process


def simple_datatable(request):
    # get json data
    data = {'data': [
        {
            'field1': '1',
            'field2': '1',
            'field3': '1',
            'field4': '1',
            'field5': '1',
        },
        {
            'field1': '12',
            'field2': '13',
            'field3': '14',
            'field4': '15',
            'field5': '23',
        },
    ]}
    return JsonResponse(data, safe=False)


def simple_edit(request, simple_id=None):
    """
    add ,modify
    """
    if simple_id is not None:
        simple = SimpleCommand().simple_get(simple_id)
    else:
        simple = None
    action = 'create' if simple is None else 'modify'
    if request.method == 'POST':
        form = SimpleForm(request.POST, initial=simple)
        if form.is_valid():
            data = form.cleaned_data
            try:
                # save data----
                simple_id = SimpleCommand(data=data).simple_edit(simple_id)
                messages.add_message(request, messages.INFO, u'simple保存成功')
                if request.POST.get('_new', None):
                    return redirect('simple:simple_create')
                return redirect('simple:simple_modify', simple_id)
            except Exception as e:
                form.add_error(None, u'保存出错')
    else:
        form = SimpleForm(simple)
    http_content = {
        'title': u'新增example' if simple_id is None else u'example详情页',
        'action': action,
        'form': form,
    }
    readonly_fields = {'readonly_fields': ['f1', 'f2']}
    if simple_id:
        http_content.update(readonly_fields)
    return render(request, t_dir + 'simple_form.html', http_content)