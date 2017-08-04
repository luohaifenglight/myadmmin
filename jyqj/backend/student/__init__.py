#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .models import StudentClassRecord


class StudentCommand(object):

    @classmethod
    def create(cls, **kwargs):
        kwargs['classes_id'] = kwargs.pop('class_id')
        kwargs['command'] = 0
        StudentClassRecord.objects.create(**kwargs)

    @classmethod
    def remove(cls, **kwargs):
        kwargs['classes_id'] = kwargs.pop('class_id')
        kwargs['command'] = 1
        StudentClassRecord.objects.create(**kwargs)

    @classmethod
    def move_in(cls, **kwargs):
        kwargs['classes_id'] = kwargs.pop('class_id')
        kwargs['command'] = 2
        StudentClassRecord.objects.create(**kwargs)

    @classmethod
    def move_out(cls, **kwargs):
        kwargs['classes_id'] = kwargs.pop('class_id')
        kwargs['command'] = 3
        StudentClassRecord.objects.create(**kwargs)

    @classmethod
    def get_all_record(cls, student_id):
        from .enumtype import *
        from .models import StudentClass
        from utils import getformattime
        all_record = StudentClassRecord.objects.filter(student_id=student_id).order_by('-id')
        data = []
        for rec in all_record:
            current_rec = {
                'class_name': rec.classes.name,
                'class_status': CLASS_STATUS.getDesc(rec.classes.class_status),
                'teacher': rec.classes.teacher.name,
                'command': COMMAND_STATUS.getDesc(rec.command),
                'create_time': getformattime(rec.create_time)
            }
            data.append(current_rec)
        return data





