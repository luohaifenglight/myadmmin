#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import IntegrityError
from django.db.models import Q
from utils.dataquery import DataBuilder, DataSQLQuery
from utils.dict_mixin import to_dict
from .models import CourseCoordinate
from backend.institution.models import CourseSystem

import traceback


class CourseSystemDB(DataBuilder):
    def getval_coordinate_num(self, obj, default=''):
        return obj.course_coordinate.all().count()

    def getval_course_num(self, obj, default=''):
        return obj.courses.filter(status=1).count()


class CourseSystemDQ(DataSQLQuery):
    model = CourseSystem
    data_model = CourseSystemDB
    pass


class CourseSystemCommand:
    def __init__(self, data=None):
        self.data = data

    def course_system_edit(self, course_system_id=None):
        course_system_info = self.data
        if course_system_info is None:
            return None
        coordinates = course_system_info.pop('coordinates', [])
        if course_system_id is None:
            exit_sys = CourseSystem.objects.filter(name=course_system_info.get('name', ''))
            if exit_sys:
                return -2
            try:
                course_system = CourseSystem.objects.create(**course_system_info)
            except IntegrityError:
                traceback.print_exc()
                print 'error'
        else:
            exit_sys = CourseSystem.objects.filter(name=course_system_info.get('name', '')).exclude(id=course_system_id)
            if exit_sys:
                return -2
            try:
                course_system = CourseSystem.objects.get(id=course_system_id)
            except:
                traceback.print_exc()
                print 'error'
                return -1
            for k, v in course_system_info.iteritems():
                setattr(course_system, k, v)
            course_system.save()
        course_system.course_coordinate.all().delete()
        if coordinates:
            for seg in coordinates:
                seg['course_system_id'] = course_system.id
                CourseCoordinate.objects.create(**seg)
        return course_system.id

    def course_system_get(self, course_system_id):
        """
        GET LIST BY id
        """
        if course_system_id is None:
            return None
        try:
            course_system = CourseSystem.objects.get(id=course_system_id)
        except IntegrityError:
            print 'error'
        cooridinate_all = course_system.course_coordinate.all()
        course_system_data = to_dict(course_system)
        cooridinate_data = [
            to_dict(v)
            for v in cooridinate_all]
        print course_system_data
        course_system_data['coordinates'] = cooridinate_data
        return course_system_data

