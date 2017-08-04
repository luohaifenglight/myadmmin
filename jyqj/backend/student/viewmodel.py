#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import IntegrityError
from django.db.models import Q
from django.db import connection
from utils.dataquery import DataBuilder, DataSQLQuery
from utils.dict_mixin import to_dict
from utils import getformattime
from .models import Student, StudentClass
from . import StudentCommand as stc

import traceback


class StudentDB(DataBuilder):

    def getval_create_time(self, obj, default=''):
        return getformattime(obj.create_time) \
            if obj.create_time else ''

    def getval_classes_name(self, obj, default=''):
        print obj.classes.all()
        return obj.classes.filter(class_status=0)[0].name


class StudentDQ(DataSQLQuery):
    model = Student
    data_model = StudentDB
    pass


class StudentCommand:
    def __init__(self, data=None):
        self.data = data

    def student_edit(self, student_id=None):
        score_optionals = self.data
        if score_optionals is None:
            return None
        if student_id is None:
            return None
        try:
            studentes = Student.objects.get(id=student_id)
        except IntegrityError:
            print 'error'
            raise IntegrityError
            studentes.score_optional.all().delete()
        try:
            for score in score_optionals:
                ScoreOptional.objects.create(**score)
        except:
            print 'error'
            raise
        return student_id

    def student_get(self, student_id):
        """
        GET LIST BY id
        """
        if student_id is None:
            return None
        try:
            studentes = Student.objects.get(id=student_id)
        except IntegrityError:
            print 'error'
        student_data = to_dict(studentes)
        count_result = self.get_count_num(student_id)
        student_data['create_time'] = getformattime(student_data['create_time']) if student_data['create_time'] else ''
        student_data['course_nums'] = count_result[0][0]
        student_data['game_bkp_level'] = count_result[1][0]
        student_data['game_bkp_coin_num'] = count_result[1][1]
        student_data['game_ballon_level'] = '%s/%s'%(count_result[2][0], count_result[2][1])
        student_data['game_ballon_coin_num'] = count_result[2][2]
        return student_data

    def get_count_num(self, student_id):
        sql_num = '''select count(*) from tb_course_class left join tb_class on tb_course_class.class_id = tb_class.Id

        left join tb_student_class on tb_student_class.class_id = tb_class.Id where  tb_student_class.student_id = %s
        and tb_course_class.`course_status`=1;'''
        sql_bkp = '''select `bkp_level_id`, sum(coin_num) as total_coin_num from `tb_bkp_play_record`
        where student_id = %s;'''
        sql_ballon = '''select tb_balloon_sub_level.level_id, `sub_level_id`, sum(coin_num) as total_coin_num
        from `tb_balloon_play_record` left join tb_balloon_sub_level
        on tb_balloon_sub_level.Id=tb_balloon_play_record.sub_level_id where student_id = %s;'''
        cursor = connection.cursor()
        cursor.execute(sql_num, [student_id])
        course_row = cursor.fetchone()
        cursor.execute(sql_bkp, [student_id])
        bkp_row = cursor.fetchone()
        cursor.execute(sql_ballon, [student_id])
        ballon_row = cursor.fetchone()
        return course_row, bkp_row, ballon_row

    @classmethod
    def class_move(cls, new_class_id, student_id):
        import time
        orginal_class = StudentClass.objects.filter(student_id=student_id).filter(classes__class_status=0)
        if not orginal_class:
            return -1  # current_class is None
        orginal_class_id = orginal_class[0].classes.id
        data = {
            'class_id': orginal_class_id,
            'student_id': student_id,
            'create_time': time.time(),
        }
        if StudentClass.objects.filter(classes_id=new_class_id).count() > 8:
            return -1 # chaoguo renshushangxian
        # StudentClass.objects.filter(classes_id=new_class_id).filter(classes__class_status=0)
        # 体验学生不能转到正常班级
        from backend.classes.models import Class
        if int(orginal_class[0].student.is_experience_num) == 1 and int(Class.objects.get(id=new_class_id).course_system.course_system_type) == 0:
            return -3
        StudentClass.objects.filter(classes_id=orginal_class_id).filter(student_id=student_id).delete()
        stc.move_out(**data)
        data['class_id'] = new_class_id
        data['create_time'] = time.time()
        data1 = {
            'classes_id': new_class_id,
            'student_id': student_id
        }
        StudentClass.objects.create(**data1)
        stc.move_in(**data)

    @classmethod
    def class_choices(cls, q='', page=1, num=30, student_id=None, institution_id=None, initial=None):
        page = int(page)
        num = int(num)

        if initial is not None:
            if isinstance(initial, (list, tuple)):
                qry = Q(id__in=initial)
            else:
                qry = Q(id=initial)
        else:
            qry = Q(id__contains=q) | Q(name__contains=q)
        from backend.classes.models import Class
        from django.db.models import Count
        query = Class.objects.annotate(student_num=Count('studentclass')).filter(class_status=0).filter(
            teacher__institution__id=institution_id).filter(
            student_num__lt=9).filter(qry).exclude(students__id=student_id)
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

    @classmethod
    def get_all_record(cls, student_id):
        return stc.get_all_record(student_id)

