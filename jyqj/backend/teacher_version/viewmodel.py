#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import IntegrityError
from django.db.models import Q
from utils.dataquery import DataBuilder, DataSQLQuery
from utils.dict_mixin import to_dict
from .models import TeacherVersion
from .enumtype import PUBLIC_TYPE, VERSION_TYPE
from utils import getformattime
from backend.institution.models import CourseSystem

import traceback
import time


class TeacherVersionDB(DataBuilder):

    def getval_create_time(self, obj, default=''):
        return getformattime(obj.create_time) \
            if obj.create_time else ''

    def getval_status(self, obj, default=''):
        return '已发布' if obj.status else '未发布'

    def getval_public_type(self, obj, default=''):
        return PUBLIC_TYPE.getDesc(obj.public_type)

    def getval_version_type(self, obj, default=''):
        return VERSION_TYPE.getDesc(obj.version_type)


class TeacherVersionDQ(DataSQLQuery):
        model = TeacherVersion
        data_model = TeacherVersionDB
        pass


class TeacherVersionCommand:

    def __init__(self, data=None):
        self.data = data

    def teacherversion_edit(self, teacherversion_id=None):
        teacherversion_info = self.data
        if teacherversion_info is None:
            return None
        if teacherversion_id is None:
            try:
                teacherversion_info['create_time'] = int(time.time())
                teacherversion = TeacherVersion.objects.create(**teacherversion_info)
            except IntegrityError:
                traceback.print_exc()
                print 'error'
        else:
            try:
                teacherversion = TeacherVersion.objects.get(id=teacherversion_id)
            except:
                traceback.print_exc()
                print 'error'
                return -1
            for k, v in teacherversion_info.iteritems():
                setattr(teacherversion, k, v)
            teacherversion.save()
        return teacherversion.id

    def teacherversion_get(self, teacherversion_id):
        """
        GET LIST BY id
        """
        if teacherversion_id is None:
            return None
        try:
            teacherversion = TeacherVersion.objects.get(id=teacherversion_id)
        except IntegrityError:
            print 'error'
        teacherversion_data = to_dict(teacherversion)
        return teacherversion_data

    @classmethod
    def reset_status(cls, id):
        teacherversion = TeacherVersion.objects.get(id=id)
        teacherversion.status = 1 - teacherversion.status
        teacherversion.save()
        return True

    @classmethod
    def get_last_package_code(cls):
        try:
            latest = TeacherVersion.objects.latest('create_time')
        except:
            latest = None
        return latest.package_code if latest else ''

