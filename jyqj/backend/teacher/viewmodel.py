#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import IntegrityError
from django.db.models import Q
from django.db import connection
from utils.dataquery import DataBuilder, DataSQLQuery
from utils.dict_mixin import to_dict
from .models import Teacher, City, TeacherCourseSystem
from backend.institution.models import CourseSystem, Institution


class TeacherDB(DataBuilder):

    def getval_status(self, obj, default=''):
        return '已冻结' if obj.status else '正常'

    def getval_create_time(self, obj, default=''):
        from utils import getformattime
        return getformattime(obj.create_time) \
            if obj.create_time else ''


class TeacherDQ(DataSQLQuery):
        model = Teacher
        data_model = TeacherDB
        pass


class TeacherCommand:

    def __init__(self, data=None):
        self.data = data

    def teacher_edit(self, teacher_id=None):
        teacher_info = self.data
        if teacher_info is None:
            return None
        mobile = teacher_info.pop('mobile', '')
        course_system = teacher_info.pop('course_system', [])
        teacher_info['city_id'] = teacher_info.pop('city')
        teacher = student = None
        try:
            teacher = Teacher.objects.get(mobile=mobile)
        except:
            try:
                from backend.student.models import Student
                student = Student.objects.get(mobile=mobile)
            except:
                print "NO student"
                print 'error'
                return -1
        if not teacher_id:
            print "INSTI:%s" % teacher_info['institution_id']
            try:
                current_institution = Institution.objects.get(id=teacher_info['institution_id'])
            except:
                print 'error'
                return -1
            if current_institution:
                concurrent_num = current_institution.concurrent_num
                teacher_num = current_institution.teachers.all().count()
                if teacher_num >= concurrent_num:
                    return -3
        if not teacher_id and teacher and teacher.institution_id:
            return -2
        if not teacher and student:
            # copy student to teacher
            teacher_info['password'] = student.password
            teacher_info['gender'] = student.gender
            teacher_info['mobile'] = student.mobile
            teacher = Teacher.objects.create(**teacher_info)
            push_sql = '''insert into tb_push(push_id, type) values (%s, 4)'''
            cursor = connection.cursor()
            cursor.execute(push_sql, [teacher.mobile])
        else:
            for k, v in teacher_info.iteritems():
                setattr(teacher, k, v)
            teacher.save()
        if course_system:
            new_s = set(CourseSystem.objects.filter(id__in=course_system))
            old_s = set(teacher.course_system.all())
            teacher.course_system.add(*(new_s - old_s))
            teacher.course_system.remove(*(old_s - new_s))
        return teacher.id

    def teacher_get(self, teacher_id):
        """
        GET LIST BY id
        """
        if teacher_id is None:
            return None
        try:
            teacher = Teacher.objects.get(id=teacher_id)
        except IntegrityError:
            raise IntegrityError
        teacher_data = to_dict(teacher)
        teacher_data['province'] = {
            'id': teacher.city.province.id,
            'text': teacher.city.province.name,
        } if getattr(teacher, 'city', '') else {}
        teacher_data['city_name'] = teacher.city.name if getattr(teacher, 'city', '') else ''
        return teacher_data

    @classmethod
    def get_teacher_by_mobile(cls, mobile):
        """
        GET LIST BY id
        """
        try:
            teacher = Teacher.objects.get(mobile=mobile)
            teacher_data = to_dict(teacher)
        except:
            print "NO teacher"
            try:
                from backend.student.models import Student
                student = Student.objects.get(mobile=mobile)
                teacher_data = to_dict(student)
            except:
                print "NO student"
                return {'name': ''}
        return teacher_data

    @classmethod
    def get_course(cls, id):
        groups = CourseSystem.objects.filter(teachers__id=id)
        results = [
            {
                'id': obj.id,
                'text': u'{}:{}'.format(
                    obj.id,
                    obj.name,
                ),

            } for obj in groups
            ]
        return results

    @classmethod
    def course_system_choices(cls, q='', page=1, num=30, insti_id=None, initial=None):
        page = int(page)
        num = int(num)

        if initial is not None:
            if isinstance(initial, (list, tuple)):
                qry = Q(id__in=initial)
            else:
                qry = Q(id=initial)
        else:
            qry = Q(id__contains=q) | Q(name__contains=q)

        query = CourseSystem.objects.filter(institutions__id=insti_id).filter(qry)
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
