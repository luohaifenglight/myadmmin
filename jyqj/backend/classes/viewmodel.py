#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import IntegrityError
from django.db.models import Q
from utils.dataquery import DataBuilder, DataSQLQuery
from utils.dict_mixin import to_dict
from utils import getformattime
from .models import Class
from backend.student.models import StudentClass
from backend.student import StudentCommand

import traceback


class ClassDB(DataBuilder):

    def getval_start_time(self, obj, default=''):
        return getformattime(obj.start_time, '%Y-%m-%d') \
            if obj.start_time else ''

    def getval_course_rate(self, obj, default=''):
        num = obj.classess.filter(course_status=2).count()
        return num


class ClassDQ(DataSQLQuery):
    model = Class
    data_model = ClassDB
    pass


class ClassCommand:
    def __init__(self, data=None):
        self.data = data

    def class_edit(self, class_id=None):
        class_data = self.data
        class_data['create_teacher_id'] = class_data['teacher_id'] = class_data.pop('teacher')
        class_data['course_system_id'] = class_data.pop('course_system')
        if class_data is None:
            return None
        from backend.teacher.models import TeacherCourseSystem
        teacher_c = TeacherCourseSystem.objects.filter(teacher_id=class_data['teacher_id']).filter(course_system_id=class_data['course_system_id'])
        if teacher_c.count() == 0:
            return -2
        if class_id is None:
            classes = Class.objects.create(**class_data)
        else:
            try:
                classes = Class.objects.get(id=class_id)
            except IntegrityError:
                print 'error'
                raise IntegrityError
            # 班级修改课程体系的时候如果该班级含有体验学生，则班级课程体系不能更改为正常课程体系
            experience_students = classes.students.filter(is_experience_num=1)
            from backend.institution.models import CourseSystem
            if experience_students and int(CourseSystem.objects.get(id=class_data['course_system_id']).course_system_type) == 0:
                return -3
            for k, v in class_data.iteritems():
                setattr(classes, k, v)
                classes.save()
        return classes.id

    @classmethod
    def remove_student(cls, class_id, student_id):
        data = {
            'class_id': class_id,
            'student_id': student_id
        }
        StudentClass.objects.filter(classes_id=class_id).filter(student_id=student_id).delete()
        StudentCommand.remove(**data)

    @classmethod
    def add_student(cls, class_id, mobile, inistiti):
        try:
            from backend.student.models import Student
            student = Student.objects.get(mobile=mobile)
        except:
            return -1
        if StudentClass.objects.filter(classes_id=class_id).filter(student_id=student.id):
            return -2 # REPEAT
        #正常班不能添加体验账号
        # 已经结业的班级不能添加学员
        current_class = Class.objects.get(id=class_id)
        if int(current_class.course_system.course_system_type) == 0 and int(student.is_experience_num) == 1:
            return -6
        if int(current_class.class_status) == 1:
            return -7
        all_class = student.classes.all()
        for cla in all_class:
            if not int(cla.class_status):
                return -3 #已经结业的班级
        if StudentClass.objects.filter(classes_id=class_id).count() > 8:
            return -4 #超过9个
        from backend.student.models import InstitutionExperience
        if int(student.is_experience_num):
            if InstitutionExperience.objects.filter(institution_id=inistiti).filter(student_id=student.id).count() == 0:
                return -5 #NOT CURRENT experience_student

        data = {
            'classes_id': class_id,
            'student_id': student.id
        }
        StudentClass.objects.create(**data)
        data = {
            'class_id': class_id,
            'student_id': student.id
        }
        StudentCommand.create(**data)
        return student.id

    def class_get(self, class_id):
        """
        GET LIST BY id
        """
        if class_id is None:
            return None
        try:
            classes = Class.objects.get(id=class_id)
        except IntegrityError:
            print 'error'
        class_data = to_dict(classes)
        class_data['start_time'] = getformattime(class_data['start_time']) if class_data['start_time'] else ''
        class_data['course_system_name'] = classes.course_system.name
        class_data['course_rate'] = classes.classess.filter(course_status=2).count()
        class_data['progress'] = '%s/%s' %(class_data['course_rate'], classes.course_system.courses.count())
        class_data['teacher_name'] = classes.teacher.name
        class_data['students'] = [to_dict(s) for s in classes.students.all()]
        return class_data


def course_system_choices(q='', page=1, num=30, instituion_id=None, initial=None):
    page = int(page)
    num = int(num)

    if initial is not None:
        if isinstance(initial, (list, tuple)):
            qry = Q(id__in=initial)
        else:
            qry = Q(id=initial)
    else:
        qry = Q(id__contains=q) | Q(name__contains=q)
    from backend.institution.models import CourseSystem
    query = CourseSystem.objects.filter(institutions__id=instituion_id).filter(qry)
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


def teacher_choices(q='', page=1, num=30, instituion_id=None, initial=None):
    page = int(page)
    num = int(num)

    if initial is not None:
        if isinstance(initial, (list, tuple)):
            qry = Q(id__in=initial)
        else:
            qry = Q(id=initial)
    else:
        qry = Q(id__contains=q) | Q(name__contains=q)
    from backend.teacher.models import Teacher
    query = Teacher.objects.filter(institution_id=instituion_id).filter(qry)
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