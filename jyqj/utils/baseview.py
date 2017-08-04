#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from utils import string_bool, split_one_char


class BaseView(View):
    def json_response(self, data, status=200):
        return JsonResponse(data, safe=False, status=status)


class DataTablesView(BaseView):
    need_count = False
    global_fields = []
    rpc_api = None

    def parse_request_data(self, req_data):
        params = BrExpandedDict(req_data)
        order_list = []
        for i in range(len(params['order'])):
            order_list.append(params['order'][str(i)])
        params['order'] = order_list

        columns_list = []
        for i in range(len(params['columns'])):
            columns_list.append(params['columns'][str(i)])
        params['columns'] = columns_list

        columns = params['columns']
        srch_opts = self.search_opts(params)
        options = {
            'columns': [col['name'] for col in columns],
            'paging': {
                'start': int(params.get('start', 0)),
                'length': int(params.get('length', 10)),
                'need_count': self.need_count,
            },
            'orders': [{
                'name': columns[int(o['column'])]['name'],
                'dir': o['dir'],
                } for o in params['order']],
            'search': None,
            'filters': srch_opts['filters'],
        }
        if '_global' in srch_opts:
            options['search'] = {
                'fields': self.global_fields,
                'value': srch_opts['_global']['value'],
                'regex': srch_opts['_global']['regex'],
            }

        self.draw = params['draw']
        self.options = options

    def search_opts(self, params):
        delimiters = ', '
        search_opts = {}
        item = params['search']
        v = item['value'].strip()
        if v:
            v = split_one_char(v, delimiters)
            search_opts['_global'] = {
                'value': v if len(v) > 1 else v[0],
                'regex': string_bool(item['regex']),
            }
        columns = params['columns']
        search_opts['filters'] = []
        for col in columns:
            v = col['search']['value'].strip()
            if col['searchable'] and v:
                v = split_one_char(v, delimiters)
                search_opts['filters'].append({
                    'field': col['name'],
                    'value': v if len(v) > 1 else v[0],
                    'regex': string_bool(col['search']['regex']),
                })
        return search_opts

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(DataTablesView, self).dispatch(*args, **kwargs)

    def do_exra(self, request):
        pass

    def post(self, request):
        # parse request data
        # build for query params
        self.do_exra(request)
        self.parse_request_data(request.POST or None)
        # call rpc datatable api
        data = self.rpc_api(**self.options)
        data['draw'] = self.draw
        data['recordsTotal'] = data.get('count', 0)
        data['recordsFiltered'] = data.get('count', 0)
        return self.json_response(data)


class BrExpandedDict(dict):
    """
    A special dictionary constructor that takes a dictionary in which the keys
    may contain brackets to specify inner dictionaries. It's confusing, but this
    example should make sense.

    >>> d = BrExpandedDict({'person[1][firstname]': ['Simon'], \
            'person[1][lastname]': ['Willison'], \
            'person[2][firstname]': ['Adrian'], \
            'person[2][lastname]': ['Holovaty']})
    >>> d
    {'person': {'1': {'lastname': ['Willison'], 'firstname': ['Simon']},
                '2': {'lastname': ['Holovaty'], 'firstname': ['Adrian']}}}
    >>> d['person']
    {'1': {'lastname': ['Willison'], 'firstname': ['Simon']}, '2': {'lastname': ['Holovaty'], 'firstname': ['Adrian']}}
    >>> d['person']['1']
    {'lastname': ['Willison'], 'firstname': ['Simon']}

    """
    def __init__(self, key_to_list_mapping):
        for k, v in key_to_list_mapping.items():
            current = self
            k = k.replace(']', '')
            bits = k.split('[')
            for bit in bits[:-1]:
                current = current.setdefault(bit, {})
            # Now assign value to current position
            try:
                current[bits[-1]] = v
            except TypeError:  # Special-case if current isn't a dict.
                current = {bits[-1]: v}
