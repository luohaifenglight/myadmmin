#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import IntegrityError
from django.db.models import Q
from utils.dataquery import DataBuilder, DataSQLQuery
from utils.dict_mixin import to_dict
from .models import ScoreOptional
from .enumtype import SCORE_OPTIONAL_TYPE
from backend.score.enumtype import MUSIC_CATEGORY_TYPE
from backend.institution.models import CourseSystem

import traceback


class CourseSystemDB(DataBuilder):
    def getval_classify(self, obj, default=''):
        return '' if not obj.score_optional.all().count() else SCORE_OPTIONAL_TYPE.getDesc(obj.score_optional.all()[0].type)

    def getval_score_num(self, obj, default=''):
        return obj.score_optional.all().count()


class CourseSystemDQ(DataSQLQuery):
    model = CourseSystem
    data_model = CourseSystemDB
    pass


class CourseSystemCommand:
    def __init__(self, data=None):
        self.data = data

    def course_system_edit(self, course_system_id=None):
        score_optionals = self.data
        if score_optionals is None:
            return None
        if course_system_id is None:
            return None
        try:
            course_system = CourseSystem.objects.get(id=course_system_id)
        except IntegrityError:
            print 'error'
            raise IntegrityError
        course_system.score_optional.all().delete()
        try:
            for score in score_optionals:
                ScoreOptional.objects.create(**score)
        except:
            print 'error'
            raise
        return course_system_id

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
        score_optional_all = course_system.score_optional.all()
        course_system_data = [
            {
                'score_id': v.score.id,
                'score_text': u'{}:{}:{}'.format(
                    v.score.id,
                    MUSIC_CATEGORY_TYPE.getDesc(v.score.music_category),
                    v.score.name,
                ),
                'seq': int(v.seq),
            }
            for v in score_optional_all]
        print course_system_data
        return course_system_data

