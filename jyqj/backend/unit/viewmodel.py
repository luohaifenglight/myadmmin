#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import IntegrityError
from django.db.models import Q
from utils.dataquery import DataBuilder, DataSQLQuery
from utils.dict_mixin import to_dict
from .models import Unit, UnitSection, HomeworkPractice, HomeworkMCPractice
from .enumtype import UNIT_TYPE, SECTION_TYPE, SECTION_TYPE_MODEL
from backend.institution.models import CourseSystem
from backend.video.enumtype import VIDEO_TYPE
from backend.score.enumtype import MUSIC_CATEGORY_TYPE
from backend.musicballoon.models import BalloonSubLevel
from backend.bukaopu.models import BKPLevel
from backend.score.b00helper import B00Helper
from backend.classes.models import CourseClass

import traceback


class UnitDB(DataBuilder):
    def getval_status(self, obj, default=''):
        return '已发布' if obj.status else '未发布'

    def getval_type(self, obj, default=''):
        return UNIT_TYPE.getDesc(obj.type)

    def getval_section_num(self, obj, default=''):
        return obj.sections.all().count()


class UnitDQ(DataSQLQuery):
    model = Unit
    data_model = UnitDB
    pass


class UnitSectionDB(DataBuilder):
    def getval_desc_type(self, obj, default=''):
        return SECTION_TYPE.getDesc(obj.type)

    def getval_name(self, obj, default=''):
        return obj.name

    def getval_is_current_use(self, obj, defalut=''):
        course_class = CourseClass.objects.filter(section_id=obj.section_id).filter(section_type=obj.type)
        print "course_class:", obj.seq, str(course_class)
        return '1' if course_class else '0'


class UnitSectionDQ(DataSQLQuery):
    model = UnitSection
    data_model = UnitSectionDB
    pass


class UnitCommand:
    def __init__(self, data=None):
        self.data = data

    def unit_edit(self, unit_id=None):
        unit_info = self.data
        if unit_info is None:
            return None
        if unit_id is None:
            try:
                unit = Unit.objects.create(**unit_info)
            except IntegrityError:
                traceback.print_exc()
                print 'error'
        else:
            try:
                unit = Unit.objects.get(id=unit_id)
            except:
                traceback.print_exc()
                print 'error'
                return -1
            for k, v in unit_info.iteritems():
                setattr(unit, k, v)
            unit.save()
        return unit.id

    def unit_get(self, unit_id):
        """
        GET LIST BY id
        """
        if unit_id is None:
            return None
        try:
            unit = Unit.objects.get(id=unit_id)
        except IntegrityError:
            print 'error'
        unit_data = to_dict(unit)
        return unit_data

    @classmethod
    def reset_status(cls, id):
        unit = Unit.objects.get(id=id)
        if int(unit.status) == 0:
            muti_units = Unit.objects.filter(status=1).filter(name=unit.name)
            if muti_units:
                return False
        unit.status = 1 - unit.status
        unit.save()
        return True

    @classmethod
    def copy(cls, id):
        unit = Unit.objects.get(id=id)
        sections = unit.sections.all()
        unit.id = None
        unit.status = 0
        unit.save()
        for section in sections:
            unit_section = SectionCommand.copy(section.id)
            unit_section.unit_id = unit.id
            unit_section.save()
        return unit.id

    @classmethod
    def unit_choices(cls, q='', page=1, num=30, initial=None):
        page = int(page)
        num = int(num)

        if initial is not None:
            if isinstance(initial, (list, tuple)):
                qry = Q(id__in=initial)
            else:
                qry = Q(id=initial)
        else:
            qry = Q(id__contains=q) | Q(name__contains=q)
        query = Unit.objects.filter(qry).filter(status=1)
        total_count = query.count()
        start_pos = (page - 1) * num
        start_pos = start_pos if start_pos >= 0 else 0
        results = [
            {
                'id': obj.id,
                'text': u'{}:{}:{}:{}'.format(
                    obj.id,
                    UNIT_TYPE.getDesc(obj.type),
                    obj.name,
                    obj.show_name,
                ),

            } for obj in query[start_pos: start_pos + num]
            ]
        return {'total_count': total_count, 'results': results, 'page': page, 'num': num}


class SectionCommand:
    def __init__(self, data=None):
        self.data = data

    def section_edit(self, unit_id=None, type=0, section_id=None):
        section_info = self.data
        if section_info is None:
            return None
        from .enumtype import SECTION_TYPE_MODEL
        section_model = SECTION_TYPE_MODEL[int(type)]
        socres = []
        score_enjoys = []
        if int(type) == 1:
            b00_path = section_info.get('b00_path', '')
            section_info['b00_syx'] = ''
            if b00_path:
                b00_syx_instance = B00Helper(b00_path)
                b00_syx = b00_syx_instance.make_b00_file()
                section_info['b00_syx'] = b00_syx
            section_info['video_id'] = section_info.pop('video', '')
            section_info['video_segment_id'] = section_info.pop('video_segment', 0) or '0'
        elif int(type) == 2:
            section_info['video_id'] = section_info.pop('video', '')
            section_info['video_segment_id'] = section_info.pop('video_segment', 0) or '0'
            section_info['score_id'] = section_info.pop('score', '')
            section_info['score_segment_id'] = section_info.pop('score_segment', '')
        elif int(type) == 3:
            section_info['score_id'] = section_info.pop('score', '')
        elif int(type) == 4:
            socres = section_info.pop('scores', [])
            score_enjoys = section_info.pop('score_enjoys', [])
        unit_section = {
            'unit_id': unit_id,
            'type': type,
        }
        if section_id is None:
            try:
                section = section_model.objects.create(**section_info)
                unit_section['section_id'] = section.id
                unitsection = UnitSection.objects.create(**unit_section)
                unitsection.seq = unitsection.id
                unitsection.save()
            except IntegrityError:
                traceback.print_exc()
                print 'error'
        else:
            try:
                section = section_model.objects.get(id=section_id)
            except:
                traceback.print_exc()
                print 'error'
                return -1
            for k, v in section_info.iteritems():
                setattr(section, k, v)
            section.save()
        if socres:
            section.sections.all().delete()
            for seg in socres:
                seg['section_id'] = section.id
                print seg
                HomeworkPractice.objects.create(**seg)
        if score_enjoys:
            section.mc_sections.all().delete()
            for seg in score_enjoys:
                seg['section_id'] = section.id
                print seg
                HomeworkMCPractice.objects.create(**seg)
        return section.id

    def section_get(self, section_id, type):
        """
        GET LIST BY id
        """
        if section_id is None:
            return None
        section_model = SECTION_TYPE_MODEL[int(type)]
        try:
            section = section_model.objects.get(id=section_id)
        except IntegrityError:
            print 'error'
        section_data = to_dict(section)
        video_options = []
        video_segment_options = []
        score_options = []
        score_segment_options = []
        game_options = []
        socres = []
        score_enjoys = []
        if isinstance(section, SECTION_TYPE_MODEL[1]) or isinstance(section, SECTION_TYPE_MODEL[2]):
            video_options.append({
                'id': section.video.id,
                'text': u'{}:{}:{}'.format(
                    section.video.id,
                    VIDEO_TYPE.getDesc(section.video.type),
                    section.video.name,
                ),
            })
            video_segment_options.append({
                'id': section.video_segment.id,
                'text': u'{}:{}'.format(
                    section.video_segment.id,
                    section.video_segment.label,
                ),
            }) if section.video_segment else ''
            section_data['video_segment'] = 2
        if isinstance(section, SECTION_TYPE_MODEL[2]):
            score_options.append({
                'id': section.score.id,
                'text': u'{}:{}:{}'.format(
                    section.score.id,
                    MUSIC_CATEGORY_TYPE.getDesc(section.score.music_category),
                    section.score.name,
                ),
            })

            score_segment_options.append({
                'id': section.score_segment.id,
                'text': u'{}:{}'.format(
                    section.score_segment.id,
                    section.score_segment.label,
                ),
            })
        if isinstance(section, SECTION_TYPE_MODEL[3]):
            score_options.append({
                'id': section.score.id,
                'text': u'{}:{}:{}'.format(
                    section.score.id,
                    MUSIC_CATEGORY_TYPE.getDesc(section.score.music_category),
                    section.score.name,
                ),
            })
        if isinstance(section, SECTION_TYPE_MODEL[4]):
            scores = section.sections.all()
            score_enjoyset = section.mc_sections.all()
            socres = [
                {
                    'score_id': obj.score.id,
                    'score_text': u'{}:{}:{}'.format(
                        obj.score.id,
                        MUSIC_CATEGORY_TYPE.getDesc(obj.score.music_category),
                        obj.score.name,
                    ),
                    'keyboard': obj.keyboard,
                    'star_num': str(obj.star_num),
                    'times': obj.times,
                    'tempo': obj.tempo,

                } for obj in scores
                ]
            score_enjoys = [
                {
                    'score_id': obj.score_enjoy.id,
                    'score_text': u'{}:{}'.format(
                        obj.score_enjoy.id,
                        obj.score_enjoy.name,
                    ),

                } for obj in score_enjoyset
            ]
        if isinstance(section, SECTION_TYPE_MODEL[5]):
            from .enumtype import GAME_TYPE
            query_set_all = BalloonSubLevel if int(section.type) == GAME_TYPE.YYQQ else BKPLevel
            game = query_set_all.objects.get(id=section.level_id)
            game_options.append({
                'id': game.id,
                'text': u'{}:{}'.format(
                    game.id,
                    game.name,
                ),
            })
        section_data['video_options'] = video_options
        section_data['video_segment_options'] = video_segment_options
        section_data['score_options'] = score_options
        section_data['score_segment_options'] = score_segment_options
        section_data['game_options'] = game_options
        section_data['scores'] = socres
        section_data['score_enjoys'] = score_enjoys
        return section_data

    @classmethod
    def reset_seq(cls, seq):
        seqs = seq.split(',')
        section_p = UnitSection.objects.get(seq=seqs[0])
        section = UnitSection.objects.get(seq=seqs[1])
        section_p.seq = seqs[1]
        section.seq = seqs[0]
        section.save()
        section_p.save()

    @classmethod
    def delete_section(cls, id):
        section = UnitSection.objects.get(id=id)
        section_type = section.type
        section_id = section.section_id
        extra_section = SECTION_TYPE_MODEL[section.type].objects.get(id=section.section_id)
        if section.type == 4:
            extra_section.sections.all().delete()
            extra_section.mc_sections.all().delete()
        extra_section.delete()
        section.delete()
        # 更新当前正在使用的该环节的数据为－1
        update_course_class(section_id, section_type)

    @classmethod
    def copy(cls, id):
        section = UnitSection.objects.get(id=id)
        extra_section = SECTION_TYPE_MODEL[section.type].objects.get(id=section.section_id)
        if section.type == 4:
            homework_practice = extra_section.sections.all()
            homework_mc_practice = extra_section.mc_sections.all()
            extra_section.id = None
            extra_section.save()
            for homework in homework_practice:
                homework.id = None
                homework.section_id = extra_section.id
                homework.save()
            for mc_homework in homework_mc_practice:
                mc_homework.id = None
                mc_homework.section_id = extra_section.id
                mc_homework.save()
        else:
            extra_section.id = None
            extra_section.save()
        section.id = None
        section.section_id = extra_section.id
        section.save()
        section.seq = section.id
        section.save()
        return section


def update_course_class(section_id, section_type):
    current_course_class = CourseClass.objects.filter(section_id=section_id).filter(section_type=section_type)
    for current in current_course_class:
        current.unit_id = -1
        current.section_id = -1
        current.section_type = -1
        current.save()


def game_choices(q='', page=1, num=30, type=1, initial=None):
    page = int(page)
    num = int(num)

    if initial is not None:
        if isinstance(initial, (list, tuple)):
            qry = Q(id__in=initial)
        else:
            qry = Q(id=initial)
    else:
        qry = Q(id__contains=q) | Q(name__contains=q)
    print type
    query_set_all, q_filter = (BalloonSubLevel, Q(Q(level_id=4) | Q(level_id=5))) if int(type) else (BKPLevel, Q(type=1))
    query = query_set_all.objects.filter(qry).filter(q_filter).filter(status=1)
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
