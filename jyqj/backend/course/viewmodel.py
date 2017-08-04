#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import IntegrityError
from django.db.models import Q
from utils.dataquery import DataBuilder, DataSQLQuery
from utils.dict_mixin import to_dict
from .models import Course, CourseUnit
from backend.institution.models import CourseSystem
from backend.unit.enumtype import UNIT_TYPE

import traceback


class CourseDB(DataBuilder):
    def getval_status(self, obj, default=''):
        return '已发布' if obj.status else '未发布'


class CourseDQ(DataSQLQuery):
    model = Course
    data_model = CourseDB
    pass


class CourseCommand:
    def __init__(self, data=None):
        self.data = data

    def course_edit(self, course_id=None):
        course_info = self.data
        if course_info is None:
            return None
        units = course_info.pop('units', [])
        name = course_info.get('name', '')
        seq = course_info.get('seq', '')
        status = int(course_info.get('status'))
        course_info['course_system_id'] = course_info.pop('course_system', '')
        if course_id is None:
            muti_name_course = Course.objects.filter(status=1).filter(name=name).filter(course_system_id=course_info['course_system_id']
                                                                    )
            if muti_name_course:
                return -2  # name muti
            muti_seq_course = Course.objects.filter(status=1).filter(seq=seq).filter(course_system_id=course_info['course_system_id'])
            if muti_seq_course and status:
                return -3  # seq muti
            try:
                course = Course.objects.create(**course_info)
            except IntegrityError:
                traceback.print_exc()
                print 'error'
        else:
            try:
                course = Course.objects.get(id=course_id)
            except:
                traceback.print_exc()
                print 'error'
                return -1
            muti_name_course = Course.objects.filter(status=1).filter(name=name).filter(course_system_id=course_info['course_system_id']
                                                                    ).exclude(id=course_id)
            if muti_name_course:
                return -2  # name muti
            muti_seq_course = Course.objects.filter(status=1).filter(seq=seq).filter(course_system_id=course_info['course_system_id']
                                                                    ).exclude(id=course_id)
            if muti_seq_course and status:
                return -3  # seq muti
            for k, v in course_info.iteritems():
                setattr(course, k, v)
            course.save()
            if not units:
                course.courseunit.all().delete()
        if units:
            course.courseunit.all().delete()
            for seg in units:
                seg['course_id'] = course.id
                CourseUnit.objects.create(**seg)
        return course.id

    def course_get(self, course_id):
        """
        GET LIST BY id
        """
        if course_id is None:
            return None
        try:
            course = Course.objects.get(id=course_id)
        except IntegrityError:
            print 'error'
        course_data = to_dict(course)
        course_unit = course.courseunit.all()
        course_data['course_unit'] = [
            {
                'unit_id': obj.unit.id,
                'unit_text': u'{}:{}:{}:{}'.format(
                    obj.unit.id,
                    UNIT_TYPE.getDesc(obj.unit.type),
                    obj.unit.name,
                    obj.unit.show_name,
                ),
                'seq': obj.seq,

            } for obj in course_unit
        ]
        course_data['course_system'] = [
            {
                'id': course.course_system.id,
                'text': u'{}:{}'.format(
                    course.course_system.id,
                    course.course_system.name,
                ),

            }
        ]
        return course_data

    @classmethod
    def reset_status(cls, id):
        course = Course.objects.get(id=id)
        if int(course.status) == 0:
            muti_name_course = Course.objects.filter(name=course.name).filter(status=1).filter(course_system_id=course.course_system_id
                                                                    )
            if muti_name_course:
                return False  # name muti
            muti_seq_course = Course.objects.filter(seq=course.seq).filter(status=1).filter(course_system_id=course.course_system_id
                                                                    )
            if muti_seq_course:
                return False
        course.status = 1 - course.status
        course.save()
        return True

    @classmethod
    def copy(cls, id):
        course = Course.objects.get(id=id)
        units = course.courseunit.all()
        course.id = None
        course.status = 0
        course.save()
        for section in units:
            section.course_id = course.id
            section.id = None
            section.save()
        return course.id
