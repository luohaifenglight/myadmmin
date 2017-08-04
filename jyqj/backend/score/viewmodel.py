#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import IntegrityError
from django.db.models import Q
from utils.dataquery import DataBuilder, DataSQLQuery
from utils.dict_mixin import to_dict
from .models import Score, ScoreSegment, ScorePic, Timbre, QnydScore
from backend.institution.models import CourseSystem
from .enumtype import MUSIC_CATEGORY_TYPE
from b00helper import B00Helper
from .score_rule import check_rule, clear_cache

import traceback


class ScoreDB(DataBuilder):
    def getval_status(self, obj, default=''):
        return '已发布' if obj.status else '未发布'

    def getval_create_time(self, obj, default=''):
        from utils import getformattime
        return getformattime(obj.create_time) \
            if obj.create_time else ''

    def getval_music_category(self, obj, default=''):
        return MUSIC_CATEGORY_TYPE.getDesc(obj.music_category)


class ScoreDQ(DataSQLQuery):
        model = Score
        data_model = ScoreDB
        pass


class ScoreCommand:

    def __init__(self, data=None):
        self.data = data

    def score_edit(self, score_id=None):
        score_info = self.data
        if score_info is None:
            return None
        segment = score_info.pop('segments', [])
        delete_id = score_info.pop('delete_id', '')
        score_images = score_info.pop('score_images', [])
        timbres = score_info.pop('timbre', [])
        b00_path = score_info.get('b00_path', '')
        smaple_midi_path = score_info.get('sample_midi_path', '')
        score_info['b00_syx'] = ''
        check_result = check_rule(score_info['compare_midi_path'], score_info['sample_midi_path'],
                                  score_info['xml_path'], segment)
        if check_result < 0:
            return check_result
        if b00_path:
            b00_syx_instance = B00Helper(b00_path)
            b00_syx = b00_syx_instance.make_b00_file()
            score_info['b00_syx'] = b00_syx
        if smaple_midi_path:
            score_info['tempo'] = B00Helper.get_tempo(smaple_midi_path)

        if score_id is None:
            try:
                score = Score.objects.create(**score_info)
            except IntegrityError:
                traceback.print_exc()
                print 'error'
        else:
            try:
                score = Score.objects.get(id=score_id)
            except:
                traceback.print_exc()
                print 'error'
                return -1
            for k, v in score_info.iteritems():
                setattr(score, k, v)
            score.save()
        delete_segment_ids = list(set(delete_id.split(',')))
        if '' in delete_segment_ids:
            delete_segment_ids.remove('')
        print "delete_ids:", delete_segment_ids
        for xx in delete_segment_ids:
            if not xx:
                continue
            try:
                ss = ScoreSegment.objects.get(id=xx)
            except:
                print 'notexit:', xx
            if ss:
                ss.delete()

       #  score_segments = ScoreSegment.objects.filter(id__in=delete_segment_ids)
        # for ss in score_segments:
        #     ss.delete()
        if segment:
            for seg in segment:
                seg['score_id'] = score.id
                if not seg['id']:
                    seg.pop('id', '')
                    ScoreSegment.objects.create(**seg)
                else:
                    segment_instance = ScoreSegment.objects.get(id=seg['id'])
                    for k, v in seg.iteritems():
                        setattr(segment_instance, k, v)
                        segment_instance.save()
        if score_images:
            score.score_images.all().delete()
            for seg in score_images:
                seg['score_id'] = score.id
                ScorePic.objects.create(**seg)
        if timbres:
            new_s = set(Timbre.objects.filter(id__in=timbres))
            old_s = set(score.timbre.all())
            score.timbre.add(*(new_s - old_s))
            score.timbre.remove(*(old_s - new_s))
        'clear score_id'
        clear_cache(score.id)
        return score.id

    def score_get(self, score_id):
        """
        GET LIST BY id
        """
        if score_id is None:
            return None
        try:
            score = Score.objects.get(id=score_id)
        except IntegrityError:
            print 'error'
        score_data = to_dict(score)
        segment_all = score.score_segments.all()
        timbres = score.timbre.all()
        score_data['segments'] = [to_dict(v) for v in segment_all]
        score_images = score.score_images.all()
        score_data['score_images'] = [to_dict(v) for v in score_images]
        score_data['timbres'] = [
            {'id': v.id, 'text': v.name} for v in timbres
        ]
        print score_data
        return score_data

    @classmethod
    def reset_status(cls, id):
        score = Score.objects.get(id=id)
        score.status = 1 - score.status
        score.save()
        return True

    @classmethod
    def delete_score(cls, id):
        score = Score.objects.get(id=id)
        from backend.unit.models import SectionSegmentPlay, SectionFullPlay, HomeworkPractice
        from utils.aes_upload import AES_Upload
        from backend.score_optional.models import ScoreOptional
        segments = SectionSegmentPlay.objects.filter(score__id=id)
        fullpalys = SectionFullPlay.objects.filter(score__id=id)
        homeworks = HomeworkPractice.objects.filter(score__id=id)
        score_optionals = ScoreOptional.objects.filter(score__id=id)
        if segments or fullpalys or homeworks or score_optionals:
            return -1
        # aes_instance = AES_Upload()
        # file_name = score.video_path.split('/')[-1]
        # aes_instance.file_upload.delete_file(('other/%s' % file_name))
        score.score_segments.all().delete()
        score.score_images.all().delete()
        score.timbre.remove(*score.timbre.all())
        score.delete()

        return True

    @classmethod
    def copy_score(cls, id):
        score = Score.objects.get(id=id)
        score_segments = score.score_segments.all()
        score_images = score.score_images.all()
        admires = score.timbre.all()
        import copy
        copy_score = copy.deepcopy(score)
        copy_score.id = None
        copy_score.status = 0
        copy_score.save()
        for score_seg in score_segments:
            score_seg.id = None
            score_seg.score_id = copy_score.id
            score_seg.save()
        for score_image in score_images:
            score_image.id = None
            score_image.score_id = copy_score.id
            score_image.save()
        copy_score.timbre.add(*admires)


        return True

def timbre_choices(q='', page=1, num=30, initial=None):
    page = int(page)
    num = int(num)

    if initial is not None:
        if isinstance(initial, (list, tuple)):
            qry = Q(id__in=initial)
        else:
            qry = Q(id=initial)
    else:
        qry = Q(id__contains=q) | Q(name__contains=q)
    query = Timbre.objects.filter(qry)
    total_count = query.count()
    start_pos = (page - 1) * num
    start_pos = start_pos if start_pos >= 0 else 0
    results = [
        {
            'id': obj.id,
            'text': u'{}:{}'.format(
                obj.id,
                obj.name,
            ),

        } for obj in query[start_pos: start_pos + num]
        ]
    return {'total_count': total_count, 'results': results, 'page': page, 'num': num}

class QnydScoreCommand:

    def __init__(self, data=None):
        self.data = data

    def score_edit(self, score_id=None):
        score_info = self.data
        if score_info is None:
            return None
        score_images = score_info.pop('score_images', [])
        qnyd_score_info = {
            'name': score_info.get('name', ''),
            'description': score_info.get('description', ''),
            'staff1_score_id': score_info.pop('staff1_score', ''),
            'staff2_score_id': score_info.pop('staff2_score', ''),
            'staff3_score_id': score_info.pop('staff3_score', ''),
            'staff1_name': score_info.pop('staff1_name', ''),
            'staff2_name': score_info.pop('staff2_name', ''),
            'staff3_name': score_info.pop('staff3_name', ''),
        }
        is_create = True
        if score_id is None:
            try:
                score = Score.objects.create(**score_info)
            except IntegrityError:
                traceback.print_exc()
                print 'error'
        else:
            is_create = False
            try:
                score = Score.objects.get(id=score_id)
            except:
                traceback.print_exc()
                print 'error'
                return -1
            for k, v in score_info.iteritems():
                setattr(score, k, v)
            score.save()
        if score_images:
            score.score_images.all().delete()
            for seg in score_images:
                seg['score_id'] = score.id
                ScorePic.objects.create(**seg)
        qnyd_score_info['whole_score_id'] = score.id
        if is_create:
            try:
                qnyd_score = QnydScore.objects.create(**qnyd_score_info)
            except IntegrityError:
                traceback.print_exc()
                print 'error'
        else:
            try:
                qnyd_score = QnydScore.objects.get(whole_score_id=score_id)
            except:
                traceback.print_exc()
                print 'error'
                return -1
            for k, v in qnyd_score_info.iteritems():
                setattr(qnyd_score, k, v)
            qnyd_score.save()
        return score.id


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
            score = Score.objects.get(id=score_id)
            qnyd_score = QnydScore.objects.get(whole_score_id=score_id)
        except IntegrityError:
            print 'error'
        score_data = to_dict(score)
        qnyd_score_data = to_dict(qnyd_score)
        score_data.update(qnyd_score_data)
        score_images = score.score_images.all()
        score_data['score_images'] = [to_dict(v) for v in score_images]
        score_data['music_office'] = [
            self.get_dict_score(getattr(qnyd_score, 'staff1_score', '')),
            self.get_dict_score(getattr(qnyd_score, 'staff2_score', '')),
            self.get_dict_score(getattr(qnyd_score, 'staff3_score', '')),
        ]
        print score_data
        return score_data


def music_office_choices(q='', music_type=0, page=1, num=30, initial=None):
    page = int(page)
    num = int(num)

    if initial is not None:
        if isinstance(initial, (list, tuple)):
            qry = Q(id__in=initial)
        else:
            qry = Q(id=initial)
    else:
        qry = Q(id__contains=q) | Q(name__contains=q)| Q(music_category__contains=q)
    qry = qry & Q(music_type=music_type) & Q(status=1)
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