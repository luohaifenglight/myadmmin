#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect

from django.db.models import Q
from django.utils.html import escape
from django.conf import settings

from utils.dict_mixin import to_dict

LIST_TYPE = (list, tuple, set)
STR_TYPE = (str, unicode)


def get_func_param_default(fn):
    fnarg = inspect.getargspec(fn)
    param_default = dict(zip(reversed(fnarg.args or []), reversed(fnarg.defaults or [])))
    return param_default


class DataBuilder(object):
    """translate an object to dict

    * **getval_xxx**

        用于获取字段的值的hook

        参数: obj
              default: 定义该字段的默认值，可不在方法中定义，默认为空字符串
              need_escape: 定义该字段值是否需要转义，可不在方法中定义，默认为True

        例: def getval_mno(self, obj, default='', need_escape=True):
                return obj.name

            def getval_pqr(self, obj, default=5):
                return obj.status

            def getval_stu(self, obj):
                return obj.id
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def build_obj_data(self, obj, fields):
        obj_data = {}
        obj_data = to_dict(obj, fields)
        if fields:
            for field in fields:
                fn_vfield = 'getval_{}'.format(field)
                fn_val = getattr(self, fn_vfield, None)
                if callable(fn_val):
                    pds = get_func_param_default(fn_val)
                    default_value = pds.get('default', '')
                    need_escape = pds.get('need_escape', True)
                    try:
                        fn_kwargs = {}
                        if 'default' in pds:
                            fn_kwargs['default'] = default_value
                        if 'need_escape' in pds:
                            fn_kwargs['need_escape'] = need_escape
                        v = fn_val(obj, **fn_kwargs)
                        if need_escape and isinstance(v, (str, unicode)):
                            v = escape(v)
                        obj_data[field] = v
                    except:
                        import traceback
                        traceback.print_exc()
                        print 'error'
                        obj_data[field] = default_value
        obj_data['pk'] = obj.id
        # for datatables
        obj_data['DT_RowId'] = u'row_{}'.format(obj.id)
        obj_data['DT_RowData'] = {'pk': unicode(obj.id)}
        return obj_data


class DataSQLQuery(object):
    """
    ## 自定义方法
    * **filter_xxx**

        用于简单过滤的hook

        参数: field: 涉及字段
              val: 查询值
              regex

        返回``Q`` object

        例: def filter_abc(self, field, val, regex):
                q = Q(status=6) & Q(is_online=True)
                return q

    * **query_xxx**

        用于复杂查询的hook

        参数: qs: 该次查询的queryset
              field
              val
              regex

        返回``queryset``

        例: def query_def(self, qs, field, val, regex):
                qs = qs.annotate(cnt_u=Count('user')).filter(cnt_u__gt=10)
                return qs

    * **order_xxx**

        用于复杂排序的字段hook

        参数: qs: 该次查询的queryset
              field
              val
              regex

        返回``queryset``

        例: def order_ghi(self, qs, field):
                qs = qs.annotate(f_rate=F('payment') - F('discount'))
                return qs, 'f_rate'
    """

    model = None
    data_model = None
    init_q = None

    def __init__(self, model=None, data_model=None, init_q=None, **kwargs):
        self.model = model or self.model
        self.data_model = data_model or self.data_model
        self.init_q = init_q or self.init_q
        self.kwargs = kwargs
        self.distinct = kwargs.get('distinct', getattr(self, 'distinct', True))

    def process(self, search=None, filters=None, nfilters=None, orders=None, paging=None, columns=None):
        """

        search: {
            'fields': [],
            'value': list or string,
            'regex': bool,
        }
        filters: [
            {'field': '', 'value': list or string, 'regex': bool},
        ]
        nfilters: [
            {'field': '', 'value': list or string, 'regex': bool},
        ]
        orders: [
            {'field': '', 'dir': 'asc' or 'desc'},
        ]
        paging: {
            'start': int, 'length': int, 'need_count': bool,
        }
        columns: [field1, field2, ...]
        """
        objs = self.build_queryset(search, filters, nfilters, orders)

        cnt = 1000
        if paging:
            # 限制每页数据的最大值
            length = paging['length'] if paging['length'] < settings.COUNT_LIMIT else settings.COUNT_LIMIT
            if paging.get('need_count', True):
                # 需要真实的结果总数
                cnt = objs.count()
                objs = objs[paging['start']: paging['start'] + length]
            else:
                size = length + 1
                objs = objs[paging['start']: paging['start'] + size]
                if len(objs) == size:
                    # 还不是最后一页
                    objs = objs[0: length]
                    cnt = paging['start'] + size
                else:
                    cnt = len(objs)
        else:
            cnt = 1000
            objs = objs[0:10]

        return self.build_resp_data(columns, cnt, objs)

    ##################################################
    # return queryset without paging
    ##################################################
    def build_queryset(self, search=None, filters=None, nfilters=None, orders=None):
        qs = self.model.objects
        qs = self.init_query(qs)
        qs = self.build_filter(qs, search, filters, nfilters)
        if self.distinct:
            qs = qs.distinct()
        qs = self.build_order(qs, orders)
        return qs

    def build_filter(self, qs, search=None, filters=None, nfilters=None):
        q = self.init_q if self.init_q is not None else Q()
        qs = qs.filter(q)
        if search:
            qs = self.global_query(qs, search)
        if filters:
            qs = self.fields_query(qs, filters)
        return qs

    def build_order(self, qs, orders=None):
        if not orders:
            return qs
        order_fields = []
        for o in orders:
            field = o['name']
            fn_ofield = 'order_{}'.format(field)
            fn_order = getattr(self, fn_ofield, None)
            if callable(fn_order):
                (qs, field) = fn_order(qs, field)
            if field:
                if o['dir'] == 'desc':
                    field = '-%s' % (field)
                order_fields.append(field)
        qs = qs.order_by(*order_fields)
        return qs

    ##################################################
    # response data
    ##################################################
    def build_resp_data(self, fields, total, objs):
        resp_data = {
            'count': total,
            'data': self.build_objs_data(objs, fields),
        }
        return resp_data

    def build_objs_data(self, objs, fields):
        builder = self.data_model(**self.kwargs)
        data = [builder.build_obj_data(obj, fields) for obj in objs]
        return data

    ##################################################
    # search
    ##################################################
    def _default_q(self, srch_key, srch_val, regex=False):
        if regex:
            # regex=True, 执行模糊搜索
            q = Q()
            if isinstance(srch_val, LIST_TYPE):
                for val in srch_val:
                    q &= Q(**{'{}__contains'.format(srch_key): val})
            else:
                q &= Q(**{'{}__contains'.format(srch_key): srch_val})
        else:
            if isinstance(srch_val, LIST_TYPE):
                key = '{}__in'.format(srch_key)
            else:
                key = srch_key
            q = Q(**{key: srch_val})
        return q

    def global_query(self, qs, gsrch):
        q = Q()
        if not gsrch:
            return qs

        fields = gsrch.get('fields', [])
        values = gsrch.get('value', None)
        regex = gsrch.get('regex', False)
        if not fields or not values:
            return qs

        if isinstance(values, STR_TYPE):
            values = [values]
        q = Q()
        for field in fields:
            q |= self._default_q(field, values, regex)
        qs = qs.filter(q)
        return qs

    def fields_query(self, qs, srch_opts):
        q = Q()
        for fsrch in srch_opts:
            field = fsrch['field']
            val = fsrch['value']
            regex = fsrch.get('regex', False)
            fname_query = 'query_{}'.format(field)
            if hasattr(self, fname_query):
                qs = getattr(self, fname_query)(qs, field, val, regex)
                continue
            fname_filter = 'filter_{}'.format(field)
            fn_filter = getattr(self, fname_filter, self._default_q)
            q &= fn_filter(field, val, regex)
        qs = qs.filter(q)
        return qs

    def _qry_time_range(self, srch_key, srch_val, regex=False):
        if not isinstance(srch_val, list) or len(srch_val) != 2:
            return Q()
        start, end = srch_val
        end = '{} 23:59:59'.format(end) if end else None
        if start and end:
            suf = 'range'
            val = [start, end]
        elif not start and not end:
            return Q()
        elif not start:
            suf = 'lt'
            val = end
        elif not end:
            suf = 'gte'
            val = start
        return Q(**{'{}__{}'.format(srch_key, suf): val})

    def init_query(self, qs):
        return qs
