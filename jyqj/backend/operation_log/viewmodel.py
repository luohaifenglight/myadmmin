#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import IntegrityError
from django.db.models import Q
from utils.dataquery import DataBuilder, DataSQLQuery
from utils.dict_mixin import to_dict
import time
from .models import OperationLog

import traceback


class OperationLogDB(DataBuilder):
    def getval_visit_time(self, obj, default=''):
        from utils import getformattime
        return getformattime(obj.visit_time) \
            if obj.visit_time else ''


class OperationLogDQ(DataSQLQuery):
        model = OperationLog
        data_model = OperationLogDB
        pass


class OperationLogCommand:

    def __init__(self, data=None):
        self.data = data

    @classmethod
    def operationlog_record(cls, request, moudle, action):
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        operationlog_info = {
            'admin_id': request.user.accountuser.id,
            'visitor_ip': ip,
            'visit_time': int(time.time()),
            'operation_path': moudle,
            'action': action,
        }
        if operationlog_info is None:
            return None
        try:
            operationlog = OperationLog.objects.create(**operationlog_info)
        except IntegrityError:
            traceback.print_exc()
            print 'error'
        return operationlog.id
