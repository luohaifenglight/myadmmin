#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import IntegrityError
from django.db.models import Q
from utils.dataquery import DataBuilder, DataSQLQuery
from utils.dict_mixin import to_dict
from .models import Score, ScoreSegment, ScorePic, Timbre, QnydScore
from backend.institution.models import CourseSystem
from backend.score.enumtype import MUSIC_CATEGORY_TYPE

import traceback


class HZQScoreDB(DataBuilder):
   pass


class HZQScoreDQ(DataSQLQuery):
        model = QnydScore
        data_model = HZQScoreDB
        pass

class QnydScoreCommand:

    def __init__(self, data=None):
        self.data = data

    def score_edit(self, score_id=None):
        score_info = self.data
        if score_info is None:
            return None
        qnyd_score_info = {
            'name': score_info.get('name', ''),
            'description': score_info.get('description', ''),
            'whole_score_id': score_info.pop('whole_score', ''),
            'staff1_score_id': score_info.pop('staff1_score', ''),
            'staff2_score_id': score_info.pop('staff2_score', ''),
            'staff3_score_id': score_info.pop('staff3_score', ''),
            'staff1_name': score_info.pop('staff1_name', ''),
            'staff2_name': score_info.pop('staff2_name', ''),
            'staff3_name': score_info.pop('staff3_name', ''),
        }

        if not score_id:
            whole_score_count = QnydScore.objects.filter(whole_score_id=qnyd_score_info['whole_score_id'])
            if whole_score_count:
                return -2  # 总谱ID已经存在
            try:
                qnyd_score = QnydScore.objects.create(**qnyd_score_info)
            except IntegrityError:
                traceback.print_exc()
                print 'error'
        else:
            whole_score_count = QnydScore.objects.filter(whole_score_id=qnyd_score_info['whole_score_id']).exclude(id=score_id)

            if whole_score_count:
                return -2  # 总谱ID已经存在
            try:
                qnyd_score = QnydScore.objects.get(id=score_id)
            except:
                traceback.print_exc()
                print 'error'
                return -1
            for k, v in qnyd_score_info.iteritems():
                setattr(qnyd_score, k, v)
            qnyd_score.save()
        return qnyd_score.id


    def get_dict_score(self, modal_instance):
        dic = {
            'id': modal_instance.id,
            'text': u'{}:{}:{}'.format(
                modal_instance.id,
                MUSIC_CATEGORY_TYPE.getDesc(modal_instance.music_category),
                modal_instance.name,
            ),
        } if modal_instance else {}
        return dic


    def score_get(self, score_id):
        """
        GET LIST BY id
        """
        if score_id is None:
            return None
        try:
            qnyd_score = QnydScore.objects.get(id=score_id)
        except IntegrityError:
            print 'error'
        qnyd_score_data = to_dict(qnyd_score)
        qnyd_score_data['music_office'] = [
            self.get_dict_score(getattr(qnyd_score, 'staff1_score', '')),
            self.get_dict_score(getattr(qnyd_score, 'staff2_score', '')),
            self.get_dict_score(getattr(qnyd_score, 'staff3_score', '')),
            self.get_dict_score(getattr(qnyd_score, 'whole_score', ''))
        ]
        print qnyd_score_data
        return qnyd_score_data


def music_office_choices(q='', page=1, num=30, initial=None):
    page = int(page)
    num = int(num)

    if initial is not None:
        if isinstance(initial, (list, tuple)):
            qry = Q(id__in=initial)
        else:
            qry = Q(id=initial)
    else:
        qry = Q(id__contains=q) | Q(name__contains=q)| Q(music_category__contains=q)
    qry = qry & Q(music_type=0) & Q(status=1)
    query = Score.objects.filter(qry)
    total_count = query.count()
    start_pos = (page - 1) * num
    start_pos = start_pos if start_pos >= 0 else 0
    results = [
        {
            'id': obj.id,
            'text': u'{}:{}:{}'.format(
                obj.id,
                MUSIC_CATEGORY_TYPE.getDesc(obj.music_category),
                obj.name,
            ),

        } for obj in query[start_pos: start_pos + num]
        ]
    return {'total_count': total_count, 'results': results, 'page': page, 'num': num}


def all_choices(q='', page=1, num=30, initial=None):
    page = int(page)
    num = int(num)

    if initial is not None:
        if isinstance(initial, (list, tuple)):
            qry = Q(id__in=initial)
        else:
            qry = Q(id=initial)
    else:
        qry = Q(id__contains=q) | Q(name__contains=q)| Q(music_category__contains=q)
    qry = qry & Q(status=1)
    query = Score.objects.filter(qry)
    total_count = query.count()
    start_pos = (page - 1) * num
    start_pos = start_pos if start_pos >= 0 else 0
    results = [
        {
            'id': obj.id,
            'text': u'{}:{}:{}'.format(
                obj.id,
                MUSIC_CATEGORY_TYPE.getDesc(obj.music_category),
                obj.name,
            ),

        } for obj in query[start_pos: start_pos + num]
        ]
    return {'total_count': total_count, 'results': results, 'page': page, 'num': num}

def segment_choices(q='', page=1, num=30, score=None, initial=None):
    page = int(page)
    num = int(num)

    if initial is not None:
        if isinstance(initial, (list, tuple)):
            qry = Q(id__in=initial)
        else:
            qry = Q(id=initial)
    else:
        qry = Q(id__contains=q) | Q(label__contains=q)
    qry = qry & Q(score__id=score)
    query = ScoreSegment.objects.filter(qry)
    total_count = query.count()
    start_pos = (page - 1) * num
    start_pos = start_pos if start_pos >= 0 else 0
    results = [
        {
            'id': obj.id,
            'text': u'{}:{}'.format(
                obj.id,
                obj.label,
            ),

        } for obj in query[start_pos: start_pos + num]
        ]
    return {'total_count': total_count, 'results': results, 'page': page, 'num': num}